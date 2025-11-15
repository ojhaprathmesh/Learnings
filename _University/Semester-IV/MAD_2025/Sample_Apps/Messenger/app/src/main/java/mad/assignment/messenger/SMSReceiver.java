package mad.assignment.messenger;

import android.annotation.SuppressLint;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsMessage;

public class SMSReceiver extends BroadcastReceiver {
    @SuppressLint("UnsafeProtectedBroadcastReceiver")
    @Override
    public void onReceive(Context context, Intent intent) {
        Bundle extras = intent.getExtras();
        if (extras == null) return;

        Object[] pdus = (Object[]) extras.get("pdus");
        if (pdus == null || pdus.length == 0) return;

        StringBuilder messageBuilder = new StringBuilder();

        for (Object pdu : pdus) {
            SmsMessage sms = SmsMessage.createFromPdu((byte[]) pdu);
            messageBuilder
                    .append("From: ").append(sms.getDisplayOriginatingAddress()).append("\n")
                    .append("Message: ").append(sms.getMessageBody()).append("\n");
        }

        if (MainActivity.instance != null) {
            MainActivity.instance.updateReceivedText(messageBuilder.toString());
        }
    }
}
