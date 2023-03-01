import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TServer.Args;
import org.apache.thrift.server.TSimpleServer;
import org.apache.thrift.transport.TServerSocket;
import org.apache.thrift.transport.TServerTransport;

import chavevalor.*;

public class ChaveValorServer {


  public static void main(String [] args) {
    try {
      ChaveValorHandler handler = new ChaveValorHandler();
      ChaveValor.Processor processor = new ChaveValor.Processor(handler);

      TServerTransport serverTransport = new TServerSocket(9090);
      TServer server = new TSimpleServer(new Args(serverTransport).processor(processor));

      System.out.println("Starting the simple server...");
      server.serve();
    } catch (Exception x) {
      x.printStackTrace();
    }
  }

}
