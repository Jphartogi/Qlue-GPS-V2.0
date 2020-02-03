
# import cv2
# import time
# import base64
# import serial
# import yaml

# ser = serial.Serial('/dev/ttyS0',115200)
# ser.flushInput()
# image_path = '/home/pi/Qlue-SIM/script/pictures/'

# Protocol = 'TCP'
# ServerIP = 'tcp.ngrok.io'
# Port = '12594'


# def initialize():
# 	#send_at('AT+CNMP=13','OK',1)
# 	#send_at('AT+NBSC=1','OK',1)
#     send_at('AT+CIPSHUT','OK',2)
#     send_at('AT+CIPMUX=0','OK',1)

#     send_at('AT+CGATT=1','OK',2)
#     #send_at('AT+COPS?','OK',1)

#     send_at('AT+CSTT="' + 'CMNET' + '"','OK',3)
#     send_at('AT+CIICR','OK',2)
#     send_at('AT+CIFSR','OK',1)
#     send_at('AT+CIPSTART="'+ Protocol +'","' + ServerIP + '",'+ Port + '' ,'OK',5)


# def send_at(command,back,timeout):
# 	rec_buff = ''
# 	ser.write((command+'\r\n').encode())
# 	time.sleep(timeout)
# 	if ser.inWaiting():
# 		time.sleep(0.1 )
# 		rec_buff = ser.read(ser.inWaiting())
# 	if rec_buff != '':
# 		if back not in rec_buff.decode():
# 			print(command + ' ERROR')
# 			print(command + ' back:\t' + rec_buff.decode())
# 			return 0
# 		else:
# 			print(rec_buff.decode())
# 			return 1
# 	else:
# 		print(command + ' no responce')


# def takePicture():
# 	key = cv2. waitKey(1)
# 	webcam = cv2.VideoCapture(0)
# 	while True:

# 	    check, frame = webcam.read()
# 	    print(check) #prints true as long as the webcam is running

# 	    cv2.imwrite(filename=image_path +'saved_img.jpg', img=frame)
# 	    webcam.release()


# 	    #cv2.waitKey(0)
# 	    #cv2.destroyAllWindows()
# 	    print("Processing image...")
# 	    img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)

# 	    print("Resizing image to 128x128 scale...")
# 	    final_img = cv2.resize(img_,(50,50))
# 	    print("Resized...")
# 	    img_resized = cv2.imwrite(filename=image_path + 'saved_img-final.jpg', img=final_img)
# 	    print("Image saved!")
# 	    with open("test.jpg", "rb") as image_file:
# 	    	encoded_string = base64.b64encode(image_file.read())
# 	    encoded = encoded_string.decode()
# 	    if len(encoded) > 2000 and len(encoded) < 4000:
# 	    	chunks, chunk_size = len(encoded), len(encoded)//2
# 	    	a = [ encoded[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
# 	    elif len(encoded) > 4000 and len(encoded) < 6000:
# 	    	chunks, chunk_size = len(encoded), len(encoded)//3
# 	    	a = [ encoded[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
# 	    initialize = 0
# 	    print('hasil splitannya',a)
# 	    for i in a:
# 	    	sendMessage(i,initialize)
# 	    print('panjangnya bray',len(encoded))
# 	    #sendMessage(encoded)

# 	    break




# def sendMessage(msg,x):
#     if x < 1:
#         initialize()
#         x = x + 1 # to make sure just one time to initialize
#     send_at('AT+CIPSEND', '>', 5)#If not sure the message number,write the command like this: AT+CIPSEND=0, (end with 1A(hex))
#     ser.write(msg.encode())
#     if 1 == send_at(b'\x1a'.decode(),'OK',5):
# 	    print('send encode picture successfully!')
# 	    time.sleep(2)
# 	    #send_at('AT+CIPSHUT','OK',2)
# 	    #send_at('AT+CIPSTART="'+ Protocol +'","' + 'server1.qlue.id' + '",'+ '5001' + '' ,'OK',5)
# 	    time.sleep(3)



#     else:
# 	       pass
# #takePicture()
