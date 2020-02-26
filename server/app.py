import edgeiq
import socketserver
import cv2
import numpy as np


class InferenceServer(socketserver.TCPServer):
    def __init__(self, host, port, handler):
        self.timeout = 0

        self.inferencer = edgeiq.ObjectDetection(
            'alwaysai/ssd_mobilenet_v1_coco_2018_01_28')
        self.inferencer.load(edgeiq.Engine.DNN_OPENVINO)
        print('Model Loaded')

        print(f'Serving on {host}:{port}')
        super().__init__((host, port), handler)


class InferenceHandler(socketserver.BaseRequestHandler):
    def pack_msg_len(self, msg):
        return len(msg).to_bytes(4, byteorder='little')

    def unpack_msg_len(self, msg):
        return int.from_bytes(msg, byteorder='little')

    def unpack_img(self, data):
        img_buffer = np.frombuffer(data, dtype=np.uint8)
        img_buffer.resize(img_buffer.shape[0], 1)
        return cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)

    def pack_img(self, image):
        ret, img_packed = cv2.imencode('.jpg', image)
        if ret:
            return img_packed.tobytes()

        print('Failed to encode the image')
        return None

    def read(self):
        msg_length = self.unpack_msg_len(self.request.recv(4))
        chunks = []
        recvd = 0
        while recvd < msg_length:
            chunk = self.request.recv(min(msg_length - recvd, 4092))
            if chunk == b'':
                break
            chunks.append(chunk)
            recvd += len(chunk)

        return b''.join(chunks)

    def send(self, data: bytes):
        try:
            msg_len = self.pack_msg_len(data)
            print('sending data of length {}'.format(len(data)))
            self.request.sendall(msg_len)
            self.request.sendall(data)
            return True
        except Exception as e:
            print(e)
            return False

    def handle(self):
        data = self.read()

        image = self.unpack_img(data)

        results = self.server.inferencer.detect_objects(image,
                                                        confidence_level=.5)

        final = edgeiq.markup_image(image,
                                    results.predictions,
                                    colors=self.server.inferencer.colors)

        image = self.pack_img(final)

        if image is not None:
            self.send(image)


if __name__ == "__main__":
    with InferenceServer('', 5000, InferenceHandler) as server:
        server.serve_forever()
