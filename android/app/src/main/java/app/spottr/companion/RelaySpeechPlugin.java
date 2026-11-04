package app.spottr.companion;

import android.Manifest;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import com.getcapacitor.JSObject;
import com.getcapacitor.PermissionState;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.annotation.Permission;
import com.getcapacitor.annotation.PermissionCallback;
import java.util.ArrayList;

/**
 * Relay's speech recognition. Uses the phone's ON-DEVICE recogniser when it has one (Pixel and other Android 12+ phones
 * with an offline English pack), so understanding what you said needs no internet. If the phone has no on-device
 * recogniser, or its English pack isn't downloaded, it falls back to the normal (online) recogniser and asks Android
 * to fetch the offline pack for next time.
 */
@CapacitorPlugin(name = "RelaySpeech", permissions = { @Permission(strings = { Manifest.permission.RECORD_AUDIO }, alias = "mic") })
public class RelaySpeechPlugin extends Plugin {
    private SpeechRecognizer rec;
    private PluginCall pending;
    private boolean triedDownload = false;
    private String lastMode = "";

    private boolean onDeviceAvailable() {
        return Build.VERSION.SDK_INT >= 31 && SpeechRecognizer.isOnDeviceRecognitionAvailable(getContext());
    }

    @PluginMethod
    public void available(PluginCall call) {
        JSObject r = new JSObject();
        r.put("onDevice", onDeviceAvailable());
        r.put("online", SpeechRecognizer.isRecognitionAvailable(getContext()));
        r.put("lastMode", lastMode);
        call.resolve(r);
    }

    @PluginMethod
    public void listen(PluginCall call) {
        if (getPermissionState("mic") != PermissionState.GRANTED) { requestPermissionForAlias("mic", call, "micGranted"); return; }
        start(call, onDeviceAvailable());
    }

    @PermissionCallback
    private void micGranted(PluginCall call) {
        if (getPermissionState("mic") != PermissionState.GRANTED) { JSObject r = new JSObject(); r.put("text", ""); r.put("error", "permission"); call.resolve(r); return; }
        start(call, onDeviceAvailable());
    }

    private Intent intent(String lang, boolean onDevice) {
        Intent i = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        i.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        i.putExtra(RecognizerIntent.EXTRA_LANGUAGE, lang);
        i.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1);
        i.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, false);
        i.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, getContext().getPackageName());
        if (onDevice) i.putExtra(RecognizerIntent.EXTRA_PREFER_OFFLINE, true);
        return i;
    }

    private void start(PluginCall call, boolean onDevice) {
        final String lang = call.getString("lang", "en-GB");
        getActivity().runOnUiThread(() -> {
            finish(null);
            pending = call;
            try {
                rec = onDevice ? SpeechRecognizer.createOnDeviceSpeechRecognizer(getContext()) : SpeechRecognizer.createSpeechRecognizer(getContext());
            } catch (Throwable e) {
                if (onDevice) { pending = null; start(call, false); return; }
                JSObject r = new JSObject(); r.put("text", ""); r.put("error", "unavailable"); pending = null; call.resolve(r); return;
            }
            final String mode = onDevice ? "on-device" : "online";
            rec.setRecognitionListener(new RecognitionListener() {
                @Override public void onResults(Bundle b) {
                    ArrayList<String> m = b.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
                    JSObject r = new JSObject(); r.put("text", m != null && !m.isEmpty() ? m.get(0) : ""); r.put("mode", mode);
                    lastMode = mode; finish(r);
                }
                @Override public void onError(int code) {
                    // the English pack isn't on the phone yet: ask Android to download it, and use the online recogniser this time
                    boolean packMissing = code == 12 || code == 13;  // LANGUAGE_NOT_SUPPORTED, LANGUAGE_UNAVAILABLE
                    if (onDevice && (packMissing || code == SpeechRecognizer.ERROR_CLIENT || code == SpeechRecognizer.ERROR_SERVER)) {
                        if (packMissing && !triedDownload && Build.VERSION.SDK_INT >= 33) {
                            triedDownload = true;
                            try { rec.triggerModelDownload(intent(lang, true)); } catch (Throwable ignored) {}
                        }
                        PluginCall c = pending; pending = null; destroy(); start(c, false); return;
                    }
                    JSObject r = new JSObject(); r.put("text", ""); r.put("mode", mode);
                    r.put("error", code == SpeechRecognizer.ERROR_NO_MATCH || code == SpeechRecognizer.ERROR_SPEECH_TIMEOUT ? "" :
                                   code == SpeechRecognizer.ERROR_NETWORK || code == SpeechRecognizer.ERROR_NETWORK_TIMEOUT ? "network" :
                                   code == SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS ? "permission" : "code " + code);
                    lastMode = mode; finish(r);
                }
                @Override public void onReadyForSpeech(Bundle b) { notifyListeners("ready", new JSObject()); }
                @Override public void onBeginningOfSpeech() {}
                @Override public void onRmsChanged(float v) {}
                @Override public void onBufferReceived(byte[] b) {}
                @Override public void onEndOfSpeech() {}
                @Override public void onPartialResults(Bundle b) {}
                @Override public void onEvent(int t, Bundle b) {}
            });
            rec.startListening(intent(lang, onDevice));
        });
    }

    private void destroy() { if (rec != null) { try { rec.destroy(); } catch (Throwable ignored) {} rec = null; } }

    /** resolve the waiting call (if any) and release the recogniser */
    private void finish(JSObject r) {
        PluginCall c = pending; pending = null;
        destroy();
        if (c != null) { if (r == null) { r = new JSObject(); r.put("text", ""); r.put("error", "replaced"); } c.resolve(r); }
    }

    @PluginMethod
    public void stop(PluginCall call) {
        getActivity().runOnUiThread(() -> { if (rec != null) { try { rec.stopListening(); } catch (Throwable ignored) {} } finish(null); call.resolve(); });
    }
}
