import mediapipe as mp
import cv2
import math


class HandDetection:
    """
    Finds Hands using the mediapipe library. Exports the landmarks
    in pixel format. Adds extra functionalities like finding how
    many fingers are up or the distance between two fingers. Also
    provides bounding box info of the hand found.
    """

    def __init__(self, mode:bool = False, maxHands:int = 2, detectionCon:float = 0.5, minTrackCon:float = 0.5):
        """
        -> mode: Static mode(True), detection is done on each image: slower else fast(False)
        -> maxHands: Maximum number of hands to detect
        -> detectionCon: Minimum Detection Confidence Threshold
        -> minTrackCon: Minimum Tracking Confidence Threshold
        """

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    
    def findHands(self, frame, draw:bool=True, extraDraw:bool=False, flipType:bool=False):
        """
        Finds hands in a BGR image.
        -> frame: Frame to find the hands in.
        -> draw: Flag to draw the output on the frame.
        -> flipType: To flip the frame with respect to horizontal on True.
        \t--> return: Frame with or without drawings.
        """
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = frame.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
                    
                if extraDraw:
                    cv2.rectangle(frame, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (255, 0, 255), 2)
                    cv2.putText(frame, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
        if draw:
            return allHands, frame
        else:
            return allHands

    
    def fingersUpAndHandSide(self, myHand):
        """
        Finds how many fingers are open and returns in a list.
        Considers left and right hands separately
        \t\t--> return: List of which fingers are up \n
        \t\t\t\tHands position (Up, Down) and (Front, Back)
        """

        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            fingers = []
            handSide = "None"
            handDir = "None"


            # For Thumb
            if myHandType == "Right":
                if myLmList[self.tipIds[4] - 3][0] > myLmList[self.tipIds[0]][0]:
                    if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    
                    if self.findDistance(myLmList[self.tipIds[4] - 3][:2], myLmList[self.tipIds[0] - 2][:2])[0] >= 10:
                        handSide = "FrontR"
                        handDir = "UpR"
                    else:
                        handSide = "CenterR"

                elif myLmList[self.tipIds[4] - 3][0] < myLmList[self.tipIds[0]][0]:
                    if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    
                    if self.findDistance(myLmList[self.tipIds[4] - 3][:2], myLmList[self.tipIds[0] - 2][:2])[0] >= 10:
                        handSide = "BackR"
                        handDir = "UpR"
                    else:
                        handSide = "CenterR"

            elif myHandType == "Left":
                if myLmList[self.tipIds[4] - 3][0] > myLmList[self.tipIds[0]][0]:
                    if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                    if self.findDistance(myLmList[self.tipIds[4] - 3][:2], myLmList[self.tipIds[0]][:2])[0] >= 20:
                        handSide = "BackL"
                        handDir = "UpL"
                    else:
                        handSide = "centerL"

                elif myLmList[self.tipIds[4] - 3][0] < myLmList[self.tipIds[0]][0]:
                    if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                    if self.findDistance(myLmList[self.tipIds[4] - 3][:2], myLmList[self.tipIds[0]][:2])[0] >= 20:
                        handSide = "FrontL"
                        handDir = "UpL"
                    else:
                        handSide = "centerL"

            # 4 Fingers
            for id in range(1, 5):
                if myLmList[self.tipIds[id] - 3][1] <= myLmList[0][1]:
                    if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                elif myLmList[self.tipIds[id] - 3][1] > myLmList[0][1]:
                    if myLmList[self.tipIds[id]][1] > myLmList[self.tipIds[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    
        # SETTING HAND POSITIONS
        if myLmList[0][1] < myLmList[self.tipIds[2] - 3][1]:
            if handSide[:-1] == "Back":
                handSide = "Front" + handSide[-1]
            elif handSide[:-1] == "Front":
                handSide = "Back" + handSide[-1]
            handDir = "Down" + handDir[-1]
    
        return [fingers, [handSide, handDir]]
    

    def findDistance(self, p1, p2, img=None):
        """
        Find the distance between two landmarks based on their
        index numbers.
        -> p1: Point1
        -> p2: Point2
        -> img: Image to draw on.
        -> draw: Flag to draw the output on the image.
        \t\t--> return: Distance between the points
                 Image with output drawn
                 Line information
        """

        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if img is not None:
            cv2.circle(img, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 5, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
            return length, info, img
        else:
            return length, info