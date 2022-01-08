import cv2

cap = cv2.VideoCapture(1)
cap.set(2, 1280)
cap.set(3, 520)

while True:

    # 1. Import image
    success, img = cap.read()
    #img = cv2.flip(img, 1)


    cv2.imshow("Image", img)
    cv2.waitKey(1)
