import sys
sys.path.append("gen-py")
import os

from thrift.protocol import TBinaryProtocol
from thrift.server import TProcessPoolServer, TServer
from thrift.transport import TSocket, TTransport

from volume import OccupationService
from volume.ttypes import Response, Req
import base64
# load configuration

import configparser as ConfigParser
import Configuration

def image_to_base64(image_path):
    fin = open(image_path, "rb")
    imgb64s = base64.b64encode(fin.read())
    fin.close()
    new_base64_str = str(imgb64s, 'utf-8')
    return new_base64_str


def predict(image_name):
    config_path = "./config/config.ini"
    configuration = Configuration.Configuration(config_path)
    port = configuration.server_detail['port']
    ip = configuration.server_detail['ip']
    # Make socket
    transport = TSocket.TSocket(ip, port)
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = OccupationService.Client(protocol)
    transport.open()
    req = Req()
    base64_str = image_to_base64(image_name)
    req.base64_img = base64_str
    response = client.predict(req)
    return [response.occupation]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("<input_image_name>")
        sys.exit()

    # test img
    image_name = sys.argv[1]
    response = predict(image_name) 
    print(response)
