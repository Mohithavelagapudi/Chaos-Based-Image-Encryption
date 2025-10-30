import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import cv2
import numpy as np
import base64
from math import log


def ArnoldCatTransform(img, num):
    rows, cols, ch = img.shape
    n = rows
    img_arnold = np.zeros([rows, cols, ch])
    for x in range(0, rows):
        for y in range(0, cols):
            img_arnold[x][y] = img[(x+y)%n][(x+2*y)%n]
    return img_arnold

def ArnoldCatDecryption(imageName, key):
    img = imageName
    rows, cols, ch = img.shape
    dimension = rows
    decrypt_it = dimension
    if (dimension%2==0) and 5**int(round(log(dimension/2,5))) == int(dimension/2):
        decrypt_it = 3*dimension
    elif 5**int(round(log(dimension,5))) == int(dimension):
        decrypt_it = 2*dimension
    elif (dimension%6==0) and  5**int(round(log(dimension/6,5))) == int(dimension/6):
        decrypt_it = 2*dimension
    else:
        decrypt_it = int(12*dimension/7)
    for i in range(key,decrypt_it):
        img = ArnoldCatTransform(img, i)
    return img

def decrypt_key(private_key, encrypted_key):
    private_key_bytes = RSA.import_key(base64.b64decode(private_key))
    
    cipher = PKCS1_OAEP.new(private_key_bytes)
    decrypted_key = int.from_bytes(cipher.decrypt(encrypted_key), byteorder='big')
    return decrypted_key

def receive_image(client_socket):
    # Receive the encrypted Arnold Cat key
    private_key = 'MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDElbNLYnVoN/+yb5aqlUL2UV28dg3QaLBt7RLJf+2Zpn7ie07jctF0bsoHdZ4v6ppvryGWC0h/RSTnznRjZt0Wh9gOdqYmaydvpU8hPXUkckNU5sRLEkeGhjPhIt1xcla7smIqjHkGv8V3j+1Q0qdCR6c/5CMJ/O3D2gxpIjkxSnsWCH3g418NKRo6/JKKaY40prJzmT/z9UWkcSlG2j8+hOrFiS6svpTkzFmMsa5jVgs7SDrYymbdSeG6hNR065gvcA4o5y3WE7Tjbm6l0W3tnEL9CZjTm9dbH+YVO3nvukYfKROWJHzc2G7XjhfN2Q4/nEqa//xSvyDy5MY3Hc4HAgMBAAECggEAB/94hPJOM92bYeds/3xadhUHYESD+V0DreU9pMRh+/oBzYsWFuYz+Vhh5dMg4B2GXPwzZ0cG6GP9cA+T5/tmYU/zjVsXFWxkoAPfZ/XNJJzKz9MiXKozY24QVvIz2jVnAUns+S2FOwNlsEtDF3e1OwVum4iCQxoZk6SfvqNCz8DVUxbzJh5wArmlnExHHefIEeP+4TexE3y5zduaESJueiV5PCQ+lArRhuRVB5D2UA9stGQcpUP1/yyb2pDYSFTRm+D0BuL2lMGD8mAQbERGWy79zudUdaMbwoT5uo6ohdTBSJJbWtXUqE/B7HGJiCUQwXZKiYXPy08m7+eYdOj08QKBgQD2RiNXfALoe+6WGRz3G4XXOjGh12NdeFSM/RDYNT8E5/cOqTtyCAIaOBmWq0nM1+vlaaTRwnMbdGwJgy2zJ/+ZpmiMPkCv52j5AFEVcn/GaCOwdM57J1hHXdDnVBGjIGjeMsE2mZ5/fEynrS86FAxkW5zkIsovsQP9pnVpckPbKQKBgQDMWTKsOmpKvPqamrs19oAOgj50wyLxMAV5U2w6uSnXzmnyW7i4nY+u1kDFQi/KJcNdjjk3u52M2EdDWUskpNvvGzvPo0AZJYtmB+sOujZ8uFLvvOVwNuH55Pqb19EuKnBPka1JdicdVeF+f0PTOhw0AFETFcOstlCSqsN/im+1rwKBgAOgUsLmA5DyyjeRlRiaYiUiKTrt1fu5Wt1cmJPmbNAgrkWb/lEWhxllvBK44PRQNZwCKzgfedxsoW6ebNzXeO8FQULXY9JzQNtxwr/jGLiOLgBaJ/QuRyF94yaU2VGil4i2DJxGNMxBw0swxKJBS1Fq++tsC7gaDin8+nucAB3JAoGAPHvyWbP4niKNcpF19CUABktavSi9APKbzCt7D26bCftYtJmddVd9ndxg04Ihrw26Y8ii+vIXUgb6IN8fNLtvNbiz3WOOp2LLfem+E1/enM/aDIe2yZ4VCOhTnSkmCyoYkBSoW+QS88XltpFou+6pRmMJnEKG5moYMzFEKE4LfpUCgYA5NweVA+E1hLPQWdUSLrUa5uKZmsW9EPRYcmIOsK4RlE4/6JYRAZtV1d7F8d/1VgkHYg0D8XpFT5BPlA/jeNGTbATcLk8rRX0AoUnACuw4G0xc3k1T0otigZCv2jxu6lptI8hqdlE16C6OCyBxgKFeEpmbkHvrBYetE3HyOFkl4Q=='

    output1 = client_socket.recv(2048)
    encrypted_key = output1
    decrypted_key = decrypt_key(private_key, encrypted_key)
    
    # Send acknowledgment before receiving the second output
    client_socket.send("ACK".encode())

    # Receive the second output
    output2 = client_socket.recv(4096)
    
    encrypted_img = output2
    
    # Perform Arnold Cat Decryption
    img = cv2.imdecode(np.frombuffer(encrypted_img, dtype=np.uint8), cv2.IMREAD_COLOR)
    print(img)
    decrypted_img = ArnoldCatDecryption(img, decrypted_key)
    
    return decrypted_img

def main():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('10.12.202.202', 12346))

    # Ask the user to enter the name of the image
    image_name = input("Enter the name of the image (e.g., test.png): ")
    client_socket.send(image_name.encode())
    
    #private_key = open('private.pem', 'rb').read()
    #public_key = open('public.pem', 'rb').read()
    #client_socket.send(public_key)

    # Receive the encrypted image and decrypt it
    decrypted_img = receive_image(client_socket)
    
    # Display the decrypted image
    #cv2.imshow("Decrypted Image", decrypted_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Save the decrypted image to a file
    decrypted_image_name = "decrypted_image.png"
    cv2.imwrite(decrypted_image_name, decrypted_img)
    
    print(f"Decrypted image saved as {decrypted_image_name}")

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    main()