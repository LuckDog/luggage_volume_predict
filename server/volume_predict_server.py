
import sys
sys.path.append("gen-py")
import os

from thrift.protocol import TBinaryProtocol
from thrift.server import TProcessPoolServer, TServer
from thrift.transport import TSocket, TTransport
from volume import OccupationService
from volume.ttypes import Response

# load configuration
import configparser as ConfigParser
import Configuration

import re
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import frozen_dir
import volume_model
global configuration
global occupation_model
occupation_model = volume_model.OccupationModel("./config_data")

def base64_to_image(base64_str, image_path=None):
    #image_rgb = cv2.imread(test_img)
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data).convert("RGB")
    if image_path:
        img.save(image_path)
    return img

def base64_to_cv2(base64_data, image_path=None):
    imgData = base64.b64decode(base64_data)
    nparr = np.fromstring(imgData, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_np


class Dispatcher(object):
    def predict(self, req):
        global configuration
        img = base64_to_cv2(req.base64_img)
        tmp_img_name = "tmp.jpg"
        cv2.imwrite(tmp_img_name, img)
        global occupation_model
        score = occupation_model.predict(tmp_img_name)
        response = Response()
        response.msg = True
        response.occupation = score
        return response


if __name__ == "__main__":
    config_path = os.path.join(frozen_dir.app_path(),"config/config.ini")
    if not os.path.exists(config_path):
        print("Can't find config.ini in " + config_path +", initialization failed.")
        sys.exit()
    global configuration
    configuration = Configuration.Configuration(config_path)
    port = configuration.server_detail['port']
    workers = configuration.server_detail['workers']

    handler = Dispatcher()
    processor = OccupationService.Processor(handler)
    socket = TSocket.TServerSocket(port=port)
    transport = TTransport.TBufferedTransportFactory()
    protocal = TBinaryProtocol.TBinaryProtocolFactory()

    server = TProcessPoolServer.TProcessPoolServer(processor, socket, transport, protocal)
    server.setNumWorkers(workers)
    server.serve()
