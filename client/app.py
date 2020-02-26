import socket
import cv2
import numpy as np
import os

def pack_msg_length(data: bytes):
  return len(data).to_bytes(4, byteorder='little')

def unpack_msg_length(data: bytes):
  return int.from_bytes(data, byteorder='little')
  
def read(sock):
  msg_length = unpack_msg_length(sock.recv(4))
  print(f'received {msg_length}')
  byte_chunks = []
  bytes_recvd = 0
  while bytes_recvd < msg_length:
    byte_chunk = sock.recv(min(msg_length - bytes_recvd, 4092))
    if byte_chunk == b'':
      break
    byte_chunks.append(byte_chunk)
    bytes_recvd += len(byte_chunk)
    
  return b''.join(byte_chunks)
  
def send(sock, data: bytes):
  try:
    msg_length = pack_msg_length(data)
    sock.sendall(msg_length)
    sock.sendall(data)
    print(f'sent {len(data)}')
    return True
  except Exception as e:
    print(f'Failed to send data with exception {e}')
    
  return False
  
def unpack_image(data: bytes):
  # Convert buffer into numpy array
  img_buffer = np.frombuffer(data, dtype=np.uint8)
  # Resize to the shape cv2.imdecode expects
  img_buffer.resize(img_buffer.shape[0], 1)
  # return the unpacked image 
  return cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)
  
def pack_image(image, image_format):
  ret, img_packed = cv2.imencode(image_format, image)
  if ret:
    return img_packed
  print('Failed to encode image')
  return None
    
if __name__ == '__main__':
  # Change this value to IP Address of the server
  # If not running both the client and server on the same machine
  host = 'taipi.local'
  port = 5000
  
  images = list(map(lambda path: os.path.join('images', path), os.listdir('images')))
  
  for index, img_path in enumerate(images):  
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
      sock.connect((host, port))
      
      image = cv2.imread(img_path)
      image_format = img_path[img_path.rfind('.'):]
      
      image_data = pack_image(image, image_format)
      if image_data is None:
          break

      send(sock, image_data)
      
      recvd_data = read(sock)
      image_final = unpack_image(recvd_data)
      cv2.imwrite(f'inferenced/{index}.jpg', image_final)
      
      sock.close()  

