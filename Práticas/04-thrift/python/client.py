import sys
import glob
sys.path.append('gen-py')
#sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])

from chavevalor import ChaveValor
from chavevalor.ttypes import KeyNotFound

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def main():
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = ChaveValor.Client(protocol)

    # Connect!
    transport.open()

    print("Setting key 7")
    client.setKV(7, "chave7");

    try:
        print("Trying to read keys 1, 7 and 5")
        print("Valor para chave 1 = %s" % client.getKV(1))
        print("Valor para chave 7 = %s" % client.getKV(7))
        print("Valor para chave 5 = %s" % client.getKV(5))
    except KeyNotFound as e:
        print('KeyNotFound: %r' % e)


    # Close!
    transport.close()



if __name__ == '__main__':
    main()

