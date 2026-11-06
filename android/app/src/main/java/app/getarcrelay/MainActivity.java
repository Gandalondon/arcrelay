package app.getarcrelay;

import android.graphics.Color;
import android.os.Bundle;
import android.view.WindowManager;
import androidx.core.splashscreen.SplashScreen;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    /* Android's start icon stays up until Relay has drawn its first frame (or 2.5 s), so there's no blank flash between them */
    static volatile boolean appReady = false;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        final long t0 = System.currentTimeMillis();
        appReady = false;
        SplashScreen sp = SplashScreen.installSplashScreen(this);
        sp.setKeepOnScreenCondition(() -> !appReady && System.currentTimeMillis() - t0 < 2500);
        // hand over instantly: Android's default exit fades its icon out first, which showed as a dip to black before Relay (4 Nov)
        sp.setOnExitAnimationListener(view -> view.remove());
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
}
