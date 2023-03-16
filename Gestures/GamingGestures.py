import pyautogui
from HandDetection import HandDetection


class GamingGestures:
    def __init__(self, detector:HandDetection, trigger:int=32):
        self.detector = detector
        self.trigger = trigger
        self.CLICKED = False
        # self.HOLD = False
    

    def detectGestures(self, frame, hands):
        # TWO HANDED MODE
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
                
                elif 1 not in fingersL[3:] and 1 not in fingersR and fingersL[0] == 0 and 0 not in fingersL[1:3] and not self.CLICKED:
                    pyautogui.press("space")
                    self.CLICKED = True
                
                elif 1 not in fingersR[3:] and 1 not in fingersL and fingersR[0] == 0 and 0 not in fingersR[1:3] and not self.CLICKED:
                    pyautogui.press("e")
                    self.CLICKED = True

        return frame
