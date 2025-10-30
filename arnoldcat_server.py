import socket
import cv2
import os
import numpy as np
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import pickle

# Functions for Arnold Cat Encryption
def ArnoldCatTransform(img, num):
    rows, cols, ch = img.shape
    n = rows
    img_arnold = np.zeros([rows, cols, ch])
    for x in range(0, rows):
        for y in range(0, cols):
            img_arnold[x][y] = img[(x+y)%n][(x+2*y)%n]
    return img_arnold

def ArnoldCatEncryption(img, key):
    for i in range(0, key):
        img = ArnoldCatTransform(img, i)
    return img

def encrypt_key(public_key_pem, key):
    public_key_bytes = base64.b64decode(public_key_pem)
    
    # Convert the PEM-encoded public key to an RSA key object
    public_key = RSA.import_key(public_key_bytes)
    
    # Create a cipher object
    cipher = PKCS1_OAEP.new(public_key)
    
    # Encrypt the key
    ciphertext = cipher.encrypt(key.to_bytes(4, byteorder='big'))
    
    return ciphertext

def list_images():
    # List all image files in the current directory
    images = [f for f in os.listdir() if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return images

def serve_image(client_socket, image_name):
    img = cv2.imread(image_name)
    
    # Perform Arnold Cat Encryption with a random key between 50 and 100
    key = np.random.randint(50, 101)
    img_encrypted = ArnoldCatEncryption(img, key)
    
    # Serialize the encrypted image data using pickle
    encrypted_image_data_pickled = pickle.dumps(img_encrypted)
    
    # Encrypt the Arnold Cat key with RSA
    public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxJWzS2J1aDf/sm+WqpVC9lFdvHYN0Giwbe0SyX/tmaZ+4ntO43LRdG7KB3WeL+qab68hlgtIf0Uk5850Y2bdFofYDnamJmsnb6VPIT11JHJDVObESxJHhoYz4SLdcXJWu7JiKox5Br/Fd4/tUNKnQkenP+QjCfztw9oMaSI5MUp7Fgh94ONfDSkaOvySimmONKayc5k/8/VFpHEpRto/PoTqxYkurL6U5MxZjLGuY1YLO0g62Mpm3UnhuoTUdOuYL3AOKOct1hO0425updFt7ZxC/QmY05vXWx/mFTt577pGHykTliR83Nhu144XzdkOP5xKmv/8Ur8g8uTGNx3OBwIDAQAB'
    encrypted_key = encrypt_key(public_key, key)

    output1 = encrypted_key
    output2 = encrypted_image_data_pickled

    client_socket.send(output1)

    acknowledgment = client_socket.recv(1024).decode()
    if acknowledgment == "ACK":
        # Send the second output
        print("Received ACK. Sending image...") 
        client_socket.sendall(output2)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.69.226', 12346))
    server_socket.listen(1)

    print("Server is listening for incoming connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Send the list of available images to the client
        images_list = list_images()
        images_list_pickled = pickle.dumps(images_list)
        client_socket.send(images_list_pickled)

        # Receive the selected image name from the client
        selected_image_name = client_socket.recv(1024).decode()

        # Serve the selected image to the client
        serve_image(client_socket, selected_image_name)

        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    main()
