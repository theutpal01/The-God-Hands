import pyautogui
from HandDetection import HandDetection
import numpy as np
import cv2


class MouseGestures:
    def __init__(self, detector:HandDetection, trigger:int=32, scrollSpeed:int=10):
        self.detector = detector
        self.status = ""
        self.CLICKED = False
        self.trigger = trigger
        self.scrollSpeed = scrollSpeed
        self.DRAG = False

    
    def moveMouse(self, x, y, t):
        pyautogui.moveTo(x, y, t)

    
    def convertPoints(self, p1:tuple, screenSize:tuple, frameSize:tuple, frameMargin:tuple):
        newX = np.interp(p1[0], (frameMargin[1], frameSize[0] - frameMargin[3]), (0, screenSize[0]))
        newY = np.interp(p1[1], (frameMargin[0], frameSize[1] - frameMargin[2]), (0, screenSize[1]))
        return (newX, newY)


    def detectMovements(self, frameSize, frameMargin, frame, hands):
        # ONE HANDED CONTROLS
        if len(hands) >= 1:
            lmList = hands[0].get("lmList")
            handType = hands[0].get("type")
            fingers, handInfo = self.detector.fingersUpAndHandSide(hands[0])
            rightClickEnable = False

            if handInfo[0][:-1] == "Front" and handInfo[1][:-1] == "Up":
                cv2.rectangle(frame, (frameMargin[3], frameMargin[0]), (frameSize[0] - frameMargin[1], frameSize[1] - frameMargin[2]), (220, 255, 0), 2, 1)
                
                # FOR MOVEMENT AND MOUSE & LEFT SINGLE CLICK CONTROL & RIGHT & LEFT DOUBLE CLICK CONTROL
                if 1 not in fingers[3:4] and 0 not in fingers[1:3]:
                    dist, info, frame = self.detector.findDistance(lmList[8][:2], lmList[12][:2], frame)
                    x, y = self.convertPoints(info[-2:], pyautogui.size(), frameSize, frameMargin)

                    if dist >= self.trigger:                        
                        # PERFECTING THUMB DETECTION
                        if handType == "Right":
                            
                            if handInfo[0] == "FrontR" and handInfo[1] == "UpR":
                                if lmList[4][0] >= lmList[9][0]:
                                    rightClickEnable = False
                                elif lmList[4][0] < lmList[9][0]:
                                    rightClickEnable = True
                            
                            elif handInfo[0] == "FrontR" and handInfo[1] == "DownR":
                                if lmList[4][0] <= lmList[9][0]:
                                    rightClickEnable = False
                                elif lmList[4][0] > lmList[9][0]:
                                    rightClickEnable = True

                            elif handInfo[0] == "BackR" and handInfo[1] == "UpR":
                                if lmList[4][0] <= lmList[9][0]:
                                    rightClickEnable = False
                                elif lmList[4][0] > lmList[9][0]:
                                    rightClickEnable = True

                            elif handInfo[0] == "BackR" and handInfo[1] == "DownR":
                                if lmList[4][0] >= lmList[9][0]:
                                    rightClickEnable = False
                                elif lmList[4][0] < lmList[9][0]:
                                    rightClickEnable = True

                        elif handType == "Left":
                            
                            if handInfo[0] == "FrontL" and handInfo[1] == "UpL":
                                if lmList[4][0] <= lmList[9][0]:
                                    rightClickEnable = False
                                elif lmList[4][0] > lmList[9][0]:
                                    rightClickEnable = True
                            
                            elif handInfo[0] == "FrontL" and handInfo[1] == "DownL":
                                if lmList[4][0] >= lmList[9][0]:
                                    rightClickEnable = False
                                elif lmList[4][0] < lmList[9][0]:
                                    rightClickEnable = True

                            elif handInfo[0] == "BackL" and handInfo[1] == "UpL":
                                if lmList[4][0] >= lmList[9][0]:
                                    rightClickEnable = False
                                elif lmList[4][0] < lmList[9][0]:
                                    rightClickEnable = True

                            elif handInfo[0] == "BackL" and handInfo[1] == "DownL":
                                if lmList[4][0] <= lmList[9][0]:
                                    rightClickEnable = False
                                elif lmList[4][0] > lmList[9][0]:
                                    rightClickEnable = True
                        
                        # USE OF ANY HAND WITH INDEX AND MIDDLE FINGER UP WITH SOME DIST B/W THEM AND THE OTHER IS SHOWED TO CAMERA FOR THE PROCESS TO START
                        if fingers[0] == 0 == fingers[4] and len(hands) == 2:
                            print("DRAGGING")
                            self.DRAG = True
                            if not self.CLICKED:
                                pyautogui.mouseDown()
                                self.CLICKED = True
                            pyautogui.moveTo(x, y)


                        # USE OF ANY HAND WITH INDEX AND MIDDLE FINGER UP WITH SOME DIST B/W THEM
                        elif fingers[0] == 0 == fingers[4]:
                            print("HOVERING")
                            self.moveMouse(x, y, 0.02)
                            self.CLICKED = False


                        # USE OF ANY HAND WITH INDEX AND MIDDLE FINGER UP AND SEPARATED AND LAST FINGER SHOULD BE
                        elif fingers[0] == 0 and fingers[4] == 1 and not self.CLICKED:
                            print("DOUBLE CLICK")
                            pyautogui.doubleClick(x, y)
                            self.CLICKED = True
                            self.DRAG = False


                        # USE OF ANY HAND WITH INDEX AND MIDDLE FINGER SEPARATED AND UP AND THUMB SHOULD ALSO BE UP
                        elif fingers[0] == 1 and fingers[4] == 0 and rightClickEnable and not self.CLICKED:
                            print("RIGHT CLICK")
                            pyautogui.rightClick(x, y)
                            self.CLICKED = True
                            self.DRAG = False

                    
                    # USE OF ANY HAND WITH INDEX AND MIDDLE FINGER UP AND JOINED TOGETHER
                    else:
                        cv2.circle(frame, info[-2:], 7, (200, 220, 0), cv2.FILLED)
                        if not self.CLICKED:
                            pyautogui.leftClick(x, y)
                            self.CLICKED = True
                            self.DRAG = False
                            print("LEFT CLICK")      


                # USE OF ANY HAND WITH 4 FINGERS UP AND HAND SHOULD BE IN PALM TO CAMERA POSITION
                elif 0 not in fingers[1:] and fingers[0] == 0:
                        print("GOING UP")
                        pyautogui.scroll(self.trigger)


            # USE OF ANY HAND WITH 4 FINGERS UP AND HAND SHOULD BE IN BACK TO CAMERA POSITION
            elif handInfo[0][:-1] == "Back" and handInfo[1][:-1] == "Up":
                if 0 not in fingers[1:] and fingers[0] == 0:
                    print("GOING DOWN")
                    pyautogui.scroll(-self.trigger)

        return frame
