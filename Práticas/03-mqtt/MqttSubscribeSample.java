
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import java.sql.Timestamp;
import java.util.ArrayList;

public class MqttSubscribeSample implements MqttCallback{
    final ArrayList<MqttMessage> messages;

    public MqttSubscribeSample() {
      messages = new ArrayList<MqttMessage>();
    }

    public MqttMessage getNextMessage() {
      synchronized (messages) {
        if (messages.size() == 0) {
          try {
            messages.wait();
          }
          catch (InterruptedException e) {
            // empty
          }
        }

        if (messages.size() == 0) {
          return null;
        }
        return messages.remove(0);
      }
    }

    public void connectionLost(Throwable cause) {
      System.err.println("connection lost: " + cause.getMessage());
    }

    public void deliveryComplete(IMqttDeliveryToken token) {
      System.err.println("delivery complete");
    }

    public void messageArrived(String topic, MqttMessage message) throws Exception {
      System.out.println("message arrived: " + new String(message.getPayload()) + "'");

      synchronized (messages) {
        messages.add(message);
        messages.notifyAll();
      }
    }


  public static void main(String[] args) {
    String topic        = "sensor/temperature/+";
    int qos             = 2;
    String broker       = "tcp://broker.hivemq.com:1883";
    String clientId     = "JavaSampleSub";
    MemoryPersistence persistence = new MemoryPersistence();
    MqttMessage msg = null;
    MqttSubscribeSample mss = new MqttSubscribeSample();

    try {
      MqttClient sampleClient = new MqttClient(broker, clientId, persistence);
      sampleClient.setCallback(mss);
      MqttConnectOptions connOpts = new MqttConnectOptions();
      connOpts.setCleanSession(true);
      System.out.println("Connecting to broker: "+broker);
      sampleClient.connect(connOpts);
      System.out.println("Connected");
      sampleClient.subscribe(topic, qos);
      System.out.println("Subscribed");
      do {
        msg = mss.getNextMessage();
        System.out.println("Got: " + msg.toString());
      } while (msg != null);
      sampleClient.disconnect();
      System.out.println("Disconnected");

      System.exit(0);

    } catch(MqttException me) {
      System.out.println("reason "+me.getReasonCode());
      System.out.println("msg "+me.getMessage());
      System.out.println("loc "+me.getLocalizedMessage());
      System.out.println("cause "+me.getCause());
      System.out.println("excep "+me);
      me.printStackTrace();
    }
  }
}

