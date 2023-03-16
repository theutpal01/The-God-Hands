import pyautogui
from HandDetection import HandDetection


class KeyboardGestures:
    def __init__(self, detector:HandDetection, trigger:int=32):
        self.detector = detector
        self.trigger = trigger
        self.CLICKED = False
        self.HOLD = False

    
    def detectGestures(self, frame, hands, distTrigger):
        if len(hands) == 0:
            self.CLICKED = False
            self.HOLD = False

        elif len(hands) == 1:
            myHandType = hands[0].get("type")
            fingers, handInfo = self.detector.fingersUpAndHandSide(hands[0])

            if myHandType == "Right":

                if handInfo[0][:-1] == "Back" and handInfo[1][:-1] == "Up":

                    # ALT + F4 GESRURE (TO CLOSE)
                    if 0 not in fingers[1:] and fingers[0] == 0 and not self.CLICKED:
                        pyautogui.keyDown("alt")
                        pyautogui.keyDown("f4")
                        pyautogui.keyUp("f4")
                        pyautogui.keyUp("alt")
                        print("QUIT")
                        self.CLICKED = True
                    
                    # WIN + D GESRURE (TO SHOW/HIDE DESKTOP)
                    elif 1 not in fingers[1:] and fingers[0] == 1 and not self.CLICKED:
                        pyautogui.keyDown("win")
                        pyautogui.keyDown("d")
                        pyautogui.keyUp("d")
                        pyautogui.keyUp("win")
                        self.CLICKED = True


                elif handInfo[0][:-1] == "Front" and handInfo[1][:-1] == "Up":
                    # TAB GESTURE (TO ADD A TAB BUTTON PRESS)
                    if 1 not in fingers[1:] and fingers[0] == 1 and not self.CLICKED:
                        pyautogui.keyDown("tab")
                        pyautogui.keyUp("tab")
                        self.CLICKED = True

                    # SPACEBAR GESTURE (TO ADD A SPACE BUTTON PRESS)
                    elif 1 not in fingers[2:] and 0 not in fingers[:2] and not self.CLICKED:
                        pyautogui.keyDown("space")
                        pyautogui.keyUp("space")
                        self.CLICKED = True

                    # ENTER KEY GESTURE (TO ADD A ENTER KEY PRESS)
                    elif 0 not in fingers[1:] and fingers[0] == 0 and not self.CLICKED:
                        pyautogui.keyDown("enter")
                        pyautogui.keyUp("enter") 
                        self.CLICKED = True

            elif myHandType == "Left":
                
                if handInfo[0][:-1] == "Back" and handInfo[1][:-1] == "Up":
                    # ESC BTN GESRURE (TO CLICK ESC KEY)
                    if 0 not in fingers[1:] and fingers[0] == 0 and not self.CLICKED:
                        pyautogui.keyDown("esc")
                        pyautogui.keyDown("esc")
                        self.CLICKED = True
                    
                    # WIN GESRURE (TO OPEN UP APPLICATIONS)
                    elif 1 not in fingers[1:] and fingers[0] == 1 and not self.CLICKED:
                        pyautogui.keyDown("win")
                        pyautogui.keyUp("win")
                        self.CLICKED = True

                    # PRINT SCREEN GESTURE (FOR SCREEN SHOT)
                    elif 0 not in fingers[1:3] and fingers[0] == 0 == fingers[4] and not self.CLICKED:
                        pyautogui.keyDown("alt")
                        pyautogui.keyDown("printscr")
                        pyautogui.keyUp("printscr")
                        pyautogui.keyUp("alt")
                        self.CLICKED = True


 
            if 1 not in fingers:
                self.CLICKED = False
                self.HOLD = False

        if len(hands) == 2:
            handL, handR = None, None
            handL = hands[0] if hands[0].get("type") == "Left" else hands[1]
            handR = hands[0] if hands[0].get("type") == "Right" else hands[1]

            fingersL, handInfoL = self.detector.fingersUpAndHandSide(handL)
            fingersR, handInfoR = self.detector.fingersUpAndHandSide(handR)

            if handInfoL[0][:-1] == "Front" == handInfoR[0][:-1] and handInfoL[1][:-1] == "Up" == handInfoR[1][:-1]:

                if 1 not in fingersL and 1 not in fingersR and self.CLICKED:
                    print("RESET")
                    self.CLICKED = False

                elif 1 not in fingersR and 0 not in fingersL and not self.CLICKED:
                    pyautogui.press("left")
                    self.CLICKED = True
                
                elif 1 not in fingersL and 0 not in fingersR and not self.CLICKED:
                    pyautogui.press("right")
                    self.CLICKED = True
                
                elif ((1 not in fingersL[1:] and 1 not in fingersR and fingersL[0] == 1) or (1 not in fingersR[1:] and 1 not in fingersL and fingersR[0] == 1)) and not self.CLICKED:
                    pyautogui.press("down")
                    self.CLICKED = True
                
                elif ((1 not in fingersL[2:] and 1 not in fingersR and fingersL[0] == 0 and fingersL[1] == 1) or (1 not in fingersR[2:] and 1 not in fingersL and fingersR[0] == 0 and fingersR[1] == 1)) and not self.CLICKED:
                    pyautogui.press("up")
                    self.CLICKED = True



        return frame
