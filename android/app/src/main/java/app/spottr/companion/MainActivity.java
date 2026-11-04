package app.spottr.companion;

import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.view.WindowManager;
import androidx.core.splashscreen.SplashScreen;
import androidx.core.splashscreen.SplashScreenViewProvider;
import java.util.Locale;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    /* Android's start icon stays up until the page has loaded (or 2.5 s). Then, instead of guessing where Android drew the icon,
       we ask it: the icon's exact position goes to the page, which draws the same lines on top, and only then does the
       splash go (splashDone), so the hand-over is seamless on any phone. */
    static volatile boolean introReady = false;
    static SplashScreenViewProvider splash;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        final long t0 = System.currentTimeMillis();
        introReady = false;
        SplashScreen sp = SplashScreen.installSplashScreen(this);
        sp.setKeepOnScreenCondition(() -> !introReady && System.currentTimeMillis() - t0 < 2500);
        sp.setOnExitAnimationListener(p -> {
            splash = p;
            try {
                View icon = p.getIconView();
                View web = getBridge().getWebView();
                int[] a = new int[2], w = new int[2];
                icon.getLocationOnScreen(a); web.getLocationOnScreen(w);
                float d = getResources().getDisplayMetrics().density;
                String js = String.format(Locale.US, "window.relaySplash&&relaySplash(%.2f,%.2f,%.2f,%.2f)",
                        (a[0] - w[0]) / d, (a[1] - w[1]) / d, icon.getWidth() / d, icon.getHeight() / d);
                getBridge().getWebView().evaluateJavascript(js, null);
            } catch (Throwable e) { splashDone(); return; }
            new Handler(Looper.getMainLooper()).postDelayed(MainActivity::splashDone, 1200);  /* never leave it stuck */
        });
        registerPlugin(SystemBarsPlugin.class);
        registerPlugin(RelayVoicePlugin.class);
        registerPlugin(RelayAIPlugin.class);
        registerPlugin(RelayOfflineVoicePlugin.class);
        registerPlugin(RelaySpeechPlugin.class);
        registerPlugin(RelayWakePlugin.class);
        super.onCreate(savedInstanceState);
        // Keep the screen on while Spottr is open beside the game.
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        // No grey bar: system bars start navy, then follow the screen.
        SystemBarsPlugin.apply(getWindow(), Color.parseColor("#1C1E22"), false);
    }

    static void splashDone() {
        SplashScreenViewProvider p = splash; splash = null;
        if (p != null) { try { p.remove(); } catch (Throwable ignored) {} }
    }
}
