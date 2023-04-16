import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

#######################
brushThickness = 20
eraserThickness = 75
width = 1280 
height = 720

########################


folderPath = "Header"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
header = overlayList[0]
drawColor = (255, 0, 0)

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

#detector = htm.handDetector(detectionCon=0.65,maxHands=1)
detector = htm.handDetector()
xp, yp = 0, 0
imgCanvas = np.zeros((height, width, 3), np.uint8)

while True:

    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)
    print("img shape", np.shape(img))
    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    if len(lmList[0]) != 0:
        # tip of index and middle fingers
        #print(lmList[8])
        x1, y1 = lmList[0][8][1],lmList[0][8][2]
        x2, y2 = lmList[0][12][1],lmList[0][12][2]
       

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)
        # 4. If Selection Mode - Two finger are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("Selection Mode")
            # # Checking for the click
            if y1 < 125:
                if 250 <x1 <450:
                    header = overlayList[3]
                    drawColor = (0, 0, 255)
                elif 550 <x1 <750:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 800 <x1 <950:
                    header = overlayList[0]
                    drawColor = (255, 0, 0)
                elif 1050 <x1 <1200:
                    header = overlayList[1]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5. If Drawing Mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            print( fingers[1] and fingers[2] == False )
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            #cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1


        # # Clear Canvas when all fingers are up
        #if all (x <= 1 for x in fingers):
        #    imgCanvas = np.zeros((720, 1280, 3), np.uint8)

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    # _, imgInv = cv2.threshold(imgGray, 20, 255, cv2.THRESH_BINARY_INV)
    # imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    print("img shape", np.shape(img))
    # print("imgInv shape", np.shape(imgInv))
    # img = cv2.bitwise_and(img,imgGray)
    img = cv2.bitwise_or(img,imgCanvas)

    # Setting the header image
    img[0:125, 0:width] = header
    imS = cv2.resize(img, (width,height))
    print("imgS shape", np.shape(imS))
    # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image", imS)
    #cv2.imshow("Canvas", imgCanvas)
    #cv2.imshow("Inv", imgInv)
    cv2.waitKey(1)
