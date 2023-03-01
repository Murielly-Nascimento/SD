import chavevalor.*;

import java.lang.Thread;
import org.apache.thrift.TException;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;

public class ChaveValorClient {
  public static void main(String [] args) {
    try{ 
      TTransport transport = new TSocket("localhost", 9090);
      transport.open();
      TProtocol protocol = new  TBinaryProtocol(transport);
      ChaveValor.Client client = new ChaveValor.Client(protocol);
      System.out.println("Setting keys 1, 2, 3 and 4...");
      client.setKV(1, "chave1");
      client.setKV(2, "chave2");
      client.setKV(3, "chave3");
      client.setKV(4, "chave4");
      Thread.sleep(2000);
      System.out.println("Reading keys 1, 2  and 5...");
      System.out.println("Value for key 1 is " + client.getKV(1));
      System.out.println("Value for key 2 is " + client.getKV(2));
      System.out.println("Value for key 5 is " + client.getKV(5));
      transport.close();
    } catch (KeyNotFound k) {
      System.err.println("Key not found: " + k.getKey());
    } catch (Exception x) {
      x.printStackTrace();
    } 
  }

}
