import pyautogui
from HandDetection import HandDetection


class KeyboardGestures:
    def __init__(self, detector:HandDetection, trigger:int=32):
        self.detector = detector
        self.trigger = trigger
        self.CLICKED = False
        self.HOLD = False

    
    def detectGestures(self, frame, hands):
        if len(hands) == 0:
            self.CLICKED = False
            self.HOLD = False

        elif len(hands) == 1:
            myHandType = hands[0].get("type")
            fingers, handInfo = self.detector.fingersUpAndHandSide(hands[0])

            if myHandType == "Right":

                # RIGHT HAND'S BACK FACING THE CAMERA
                if handInfo[0][:-1] == "Back" and handInfo[1][:-1] == "Up":
                    # ALT + F4 GESRURE (TO CLOSE) - USE OF RIGHT HAND WITH 4 FINGERS UP
                    if 0 not in fingers[1:] and fingers[0] == 0 and not self.CLICKED:
                        pyautogui.keyDown("alt")
                        pyautogui.keyDown("f4")
                        pyautogui.keyUp("f4")
                        pyautogui.keyUp("alt")
                        print("QUIT")
                        self.CLICKED = True
                    
                    # WIN + D GESRURE (TO SHOW/HIDE DESKTOP) - USE OF RIGHT HAND WITH INDEX FINGER UP
                    elif 1 not in fingers[2:4] and fingers[1] == 1 and not self.CLICKED:
                        pyautogui.keyDown("win")
                        pyautogui.keyDown("d")
                        pyautogui.keyUp("d")
                        pyautogui.keyUp("win")
                        print("SHOW/HIDE DESKTOP")
                        self.CLICKED = True


                # RIGHT HAND'S PALM FACING THE CAMERA
                elif handInfo[0][:-1] == "Front" and handInfo[1][:-1] == "Up":
                    # TAB GESTURE (TO ADD A TAB BUTTON PRESS) - USE OF RIGHT HAND WITH THUMB UP
                    if 1 not in fingers[1:] and fingers[0] == 1 and not self.CLICKED:
                        pyautogui.keyDown("tab")
                        pyautogui.keyUp("tab")
                        print("TAB KEY")
                        self.CLICKED = True

                    # SPACEBAR GESTURE (TO ADD A SPACE BUTTON PRESS) - USE OF RIGHT HAND WITH INDEX FINGER UP
                    elif 1 not in fingers[2:] and fingers[0] == 0 and fingers[1] == 1 and not self.CLICKED:
                        pyautogui.keyDown("space")
                        pyautogui.keyUp("space")
                        print("SPACE KEY")
                        self.CLICKED = True

                    # ENTER KEY GESTURE (TO ADD A ENTER KEY PRESS) - USE OF RIGHT HAND WITH 4 FINGERS UP
                    elif 0 not in fingers[1:] and fingers[0] == 0 and not self.CLICKED:
                        pyautogui.keyDown("enter")
                        pyautogui.keyUp("enter") 
                        print("ENTER KEY")
                        self.CLICKED = True

            elif myHandType == "Left":
                
                if handInfo[0][:-1] == "Front" and handInfo[1][:-1] == "Up":
                    # ESC BTN GESRURE (TO CLICK ESC KEY) - USE OF LEFT HAND WITH 4 FINGERS UP
                    if 0 not in fingers[1:] and fingers[0] == 0 and not self.CLICKED:
                        pyautogui.keyDown("escape")
                        pyautogui.keyUp("escape")
                        print("ESCAPE KEY")
                        self.CLICKED = True
                    
                    # WIN GESRURE (TO OPEN UP APPLICATIONS) - USE OF LEFT HAND WITH STARTING 2 FINGERS UP
                    elif 1 not in fingers[3:] and fingers[0] == 0 and fingers[1] == 1 == fingers[2] and not self.CLICKED:
                        pyautogui.keyDown("win")
                        pyautogui.keyUp("win")
                        print("WINDOWS KEY")
                        self.CLICKED = True

                    # PRINT SCREEN GESTURE (FOR SCREEN SHOT) - USE OF LEFT HAND WITH STARTING 3 FINGERS UP
                    elif 0 not in fingers[1:4] and fingers[0] == 0 == fingers[4] and not self.CLICKED:
                        pyautogui.keyDown("win")
                        pyautogui.keyDown("printscreen")
                        pyautogui.keyUp("printscreen")
                        pyautogui.keyUp("win")
                        print("SCREENSHOT SHORTCUT")
                        self.CLICKED = True

                if handInfo[0][:-1] == "Back" and handInfo[1][:-1] == "Up":
                    # CTRL + V GESRURE (TO USE PASTE SHORTCUT) - USE OF LEFT HAND WITH 4 FINGERS UP
                    if 0 not in fingers[1:] and fingers[0] == 0 and not self.CLICKED:
                        pyautogui.keyDown("ctrl")
                        pyautogui.keyDown("v")
                        pyautogui.keyUp("v")
                        pyautogui.keyUp("ctrl")
                        print("PASTE SHORTCUT")
                        self.CLICKED = True

                    # CTRL + C GESRURE (TO USE COPY SHORTCUT) - USE OF LEFT HAND WITH STARTING 2 FINGERS UP
                    elif 1 not in fingers[3:] and fingers[0] == 0 and fingers[1] == 1 == fingers[2] and not self.CLICKED:
                        pyautogui.keyDown("ctrl")
                        pyautogui.keyDown("c")
                        pyautogui.keyUp("c")
                        pyautogui.keyUp("ctrl")
                        print("COPY SHORTCUT")
                        self.CLICKED = True

                    # CTRL + X GESTURE (TO USE CUT SHROTCUT) - USE OF LEFT HAND WITH STARTING 3 FINGERS UP
                    elif 0 not in fingers[1:4] and fingers[0] == 0 == fingers[4] and not self.CLICKED:
                        pyautogui.keyDown("ctrl")
                        pyautogui.keyDown("x")
                        pyautogui.keyUp("x")
                        pyautogui.keyUp("ctrl")
                        print("CUT SHORTCUT")
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

                # USE OF LEFT HAND 4 FINGERS
                elif 1 not in fingersR and 0 not in fingersL and not self.CLICKED:
                    pyautogui.press("left")
                    print("KEY LEFT")
                    self.CLICKED = True
                
                # USE OF RIGHT HAND 4 FINGERS
                elif 1 not in fingersL and 0 not in fingersR and not self.CLICKED:
                    pyautogui.press("right")
                    print("KEY RIGHT")
                    self.CLICKED = True
                
                # USE OF BOTH HAND THUMB
                elif 1 not in fingersL[1:]  and 1 not in fingersR[1:] and fingersL[0] == 1 == fingersR[0] and not self.CLICKED:
                    pyautogui.press("down")
                    print("KEY DOWN")
                    self.CLICKED = True
                
                # USE OF BOTH HAND INDEX FINGER
                elif 1 not in fingersL[2:] and 1 not in fingersR[2:] and fingersL[0] == 0 == fingersR[0] and fingersL[1] == 1 == fingersR[1] and not self.CLICKED:
                    pyautogui.press("up")
                    print("KEY UP")
                    self.CLICKED = True



        return frame
