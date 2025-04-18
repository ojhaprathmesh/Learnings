package mad.assignment.caller;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.telephony.TelephonyManager;
import android.util.Log;

public class CallReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        String state = intent.getStringExtra(TelephonyManager.EXTRA_STATE);
        String incoming = intent.getStringExtra(TelephonyManager.EXTRA_INCOMING_NUMBER);

        if (TelephonyManager.EXTRA_STATE_RINGING.equals(state)) {
            Log.d("CallReceiver", "Incoming call from: " + incoming);
        } else if (TelephonyManager.EXTRA_STATE_OFFHOOK.equals(state)) {
            Log.d("CallReceiver", "Call answered or outgoing");
        } else if (TelephonyManager.EXTRA_STATE_IDLE.equals(state)) {
            Log.d("CallReceiver", "Call ended or idle");
        }
    }
}
