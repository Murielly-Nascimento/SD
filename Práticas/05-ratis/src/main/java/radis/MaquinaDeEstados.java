package radis;

import java.nio.charset.Charset;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import org.apache.ratis.proto.*;
import org.apache.ratis.protocol.Message;
import org.apache.ratis.statemachine.TransactionContext;
import org.apache.ratis.statemachine.impl.BaseStateMachine;

public class MaquinaDeEstados extends BaseStateMachine {
  private final Map<String, String> key2values = new ConcurrentHashMap<>();

  @Override
  public CompletableFuture<Message> query(Message request) {
    final String[] opKey = request.getContent().toString(Charset.defaultCharset()).split(":");
    final String result = opKey[0] + ":" + key2values.get(opKey[1]);

    LOG.debug("{}: {} = {}", opKey[0], opKey[1], result);
    return CompletableFuture.completedFuture(Message.valueOf(result));
  }

  @Override
  public CompletableFuture<Message> applyTransaction(TransactionContext trx) {
    final RaftProtos.LogEntryProto entry = trx.getLogEntry();
    final String[] opKeyValue =
        entry.getStateMachineLogEntry().getLogData().toString(Charset.defaultCharset()).split(":");

    final String op = opKeyValue[0];
    String result = op + ":";

    String key = opKeyValue.length < 2 ? "" : opKeyValue[1];
    String value = opKeyValue.length < 3 ? "" : opKeyValue[2];
    switch (op) {
      case "add":
        result += key2values.put(key, value);
        break;
      case "del":
        result += key2values.remove(key);
        break;
      case "clear":
        key2values.clear();
        result += ":ok";
        break;
      default:
        result += "invalid-op";
    }
    final CompletableFuture<Message> f = CompletableFuture.completedFuture(Message.valueOf(result));

    final RaftProtos.RaftPeerRole role = trx.getServerRole();
    LOG.info("{}:{} {} {}={}", role, getId(), op, key, value);

    return f;
  }
}
