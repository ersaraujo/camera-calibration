import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
count = 0
while ret:
	
	ret, frame = cap.read()
	cv2.imshow('Imagem',frame)
	key = cv2.waitKey(1)
	if key == ord('q'):
		break
	if key == ord('s'):
		count+=1
		cv2.imwrite("image%04i.jpg" %count, frame)
cv2.destroyWindow('Imagem')