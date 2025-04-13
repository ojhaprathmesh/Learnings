package mad.assignment.messenger;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsMessage;

public class SMSReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        Bundle bundle = intent.getExtras();
        if (bundle == null) return;

        Object[] pdus = (Object[]) bundle.get("pdus");
        if (pdus == null) return;

        StringBuilder receivedMsg = new StringBuilder();

        for (Object obj : pdus) {
            SmsMessage sms = SmsMessage.createFromPdu((byte[]) obj);
            receivedMsg.append("From: ").append(sms.getDisplayOriginatingAddress()).append("\n");
            receivedMsg.append("Message: ").append(sms.getMessageBody()).append("\n");
        }

        if (MainActivity.instance != null) {
            MainActivity.instance.updateReceivedText(receivedMsg.toString());
        }
    }
}
