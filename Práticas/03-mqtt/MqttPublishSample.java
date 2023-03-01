import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import java.util.Random;

public class MqttPublishSample {

  public static void main(String[] args) {
    String topic        = "sensor/temperature/1";
    String content      = "";
    int qos             = 2;
    String broker       = "tcp://broker.hivemq.com:1883";
    String clientId     = "JavaSamplePub";
    MemoryPersistence persistence = new MemoryPersistence();

    try {
	  Random random = new Random();
      MqttClient sampleClient = new MqttClient(broker, clientId, persistence);
      MqttConnectOptions connOpts = new MqttConnectOptions();
      connOpts.setCleanSession(true);
      System.out.println("Connecting to broker: "+broker);
      sampleClient.connect(connOpts);
      System.out.println("Connected");
	  do {
		Thread.sleep(1000);
		int temp = random.ints(15, 45).findFirst().getAsInt();
		content = ""+temp;
		System.out.println("Publishing message: "+content);
		MqttMessage message = new MqttMessage(content.getBytes());
		message.setQos(qos);
		sampleClient.publish(topic, message);
        System.out.println("Message published");
	  } while(true);
      /*sampleClient.disconnect();
      System.out.println("Disconnected");
      System.exit(0);*/
    } catch(MqttException me) {
      System.out.println("reason "+me.getReasonCode());
      System.out.println("msg "+me.getMessage());
      System.out.println("loc "+me.getLocalizedMessage());
      System.out.println("cause "+me.getCause());
      System.out.println("excep "+me);
      me.printStackTrace();
    } catch(InterruptedException ie) {
	  System.out.println("erro no sleep");
	}
  }
}
