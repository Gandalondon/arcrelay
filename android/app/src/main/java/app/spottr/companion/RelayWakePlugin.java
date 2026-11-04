package app.spottr.companion;

import android.Manifest;
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import com.getcapacitor.JSObject;
import com.getcapacitor.PermissionState;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.annotation.Permission;
import com.getcapacitor.annotation.PermissionCallback;
import com.k2fsa.sherpa.onnx.FeatureConfig;
import com.k2fsa.sherpa.onnx.KeywordSpotter;
import com.k2fsa.sherpa.onnx.KeywordSpotterConfig;
import com.k2fsa.sherpa.onnx.KeywordSpotterResult;
import com.k2fsa.sherpa.onnx.OnlineModelConfig;
import com.k2fsa.sherpa.onnx.OnlineStream;
import com.k2fsa.sherpa.onnx.OnlineTransducerModelConfig;

/**
 * "Hey Relay": a small offline keyword spotter (sherpa-onnx, 3.3M-parameter English model, Apache 2.0, bundled in the app).
 * It only listens for the phrase; nothing is transcribed or sent anywhere. When it hears it, it lets go of the microphone
 * and tells the app, which then runs normal speech recognition for the question.
 */
@CapacitorPlugin(name = "RelayWake", permissions = { @Permission(strings = { Manifest.permission.RECORD_AUDIO }, alias = "mic") })
public class RelayWakePlugin extends Plugin {
    private static final int RATE = 16000;
    private KeywordSpotter kws;
    private volatile boolean running = false;
    private Thread loop;
    private volatile String lastError = "";
    private volatile long wakes = 0;

    private KeywordSpotter spotter() {
        if (kws != null) return kws;
        OnlineTransducerModelConfig t = new OnlineTransducerModelConfig();
        t.setEncoder("kws/encoder.int8.onnx");
        t.setDecoder("kws/decoder.int8.onnx");
        t.setJoiner("kws/joiner.int8.onnx");
        OnlineModelConfig m = new OnlineModelConfig();
        m.setTransducer(t);
        m.setTokens("kws/tokens.txt");
        m.setModelType("zipformer2");
        m.setNumThreads(1);
        FeatureConfig f = new FeatureConfig();
        f.setSampleRate(RATE);
        f.setFeatureDim(80);
        KeywordSpotterConfig c = new KeywordSpotterConfig();
        c.setFeatConfig(f);
        c.setModelConfig(m);
        c.setKeywordsFile("kws/keywords.txt");
        // tuned on synthetic speech: 16/16 "Hey Relay" caught, 0/32 near-misses ("Hey, really?", "Hey, relax")
        c.setKeywordsScore(1.0f);
        c.setKeywordsThreshold(0.3f);
        c.setMaxActivePaths(4);
        kws = new KeywordSpotter(getContext().getAssets(), c);
        return kws;
    }

    @PluginMethod
    public void start(PluginCall call) {
        if (getPermissionState("mic") != PermissionState.GRANTED) { requestPermissionForAlias("mic", call, "micGranted"); return; }
        begin(call);
    }

    @PermissionCallback
    private void micGranted(PluginCall call) {
        if (getPermissionState("mic") != PermissionState.GRANTED) { call.reject("permission"); return; }
        begin(call);
    }

    private void begin(PluginCall call) {
        if (running) { call.resolve(); return; }
        running = true;
        loop = new Thread(() -> {
            AudioRecord rec = null;
            OnlineStream stream = null;
            try {
                KeywordSpotter k = spotter();
                stream = k.createStream("");
                int min = AudioRecord.getMinBufferSize(RATE, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT);
                rec = new AudioRecord(MediaRecorder.AudioSource.VOICE_RECOGNITION, RATE, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT, Math.max(min, RATE * 2));
                rec.startRecording();
                short[] buf = new short[RATE / 10];  // 100 ms
                float[] f = new float[buf.length];
                while (running) {
                    int n = rec.read(buf, 0, buf.length);
                    if (n <= 0) continue;
                    for (int i = 0; i < n; i++) f[i] = buf[i] / 32768f;
                    stream.acceptWaveform(n == f.length ? f : java.util.Arrays.copyOf(f, n), RATE);
                    while (k.isReady(stream)) {
                        k.decode(stream);
                        KeywordSpotterResult r = k.getResult(stream);
                        if (r.getKeyword() != null && !r.getKeyword().isEmpty()) {
                            k.reset(stream);
                            wakes++;
                            running = false;  // let go of the microphone first, so speech recognition can have it
                            try { rec.stop(); } catch (Throwable ignored) {}
                            JSObject e = new JSObject(); e.put("keyword", r.getKeyword());
                            notifyListeners("wake", e);
                            break;
                        }
                    }
                }
            } catch (Throwable e) {
                lastError = e.getClass().getSimpleName() + ": " + e.getMessage();
                JSObject ev = new JSObject(); ev.put("error", lastError);
                notifyListeners("error", ev);
            } finally {
                running = false;
                if (rec != null) { try { rec.stop(); } catch (Throwable ignored) {} rec.release(); }
                if (stream != null) { try { stream.release(); } catch (Throwable ignored) {} }
            }
        }, "relay-wake");
        loop.start();
        call.resolve();
    }

    @PluginMethod
    public void stop(PluginCall call) {
        running = false;
        Thread t = loop;
        if (t != null) { try { t.join(600); } catch (InterruptedException ignored) {} }
        call.resolve();
    }

    @PluginMethod
    public void status(PluginCall call) {
        JSObject r = new JSObject();
        r.put("running", running);
        r.put("wakes", wakes);
        r.put("error", lastError);
        call.resolve(r);
    }
}
