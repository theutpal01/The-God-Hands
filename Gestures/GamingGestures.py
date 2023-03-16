import pyautogui
from HandDetection import HandDetection


class GamingGestures:
    def __init__(self, detector:HandDetection, trigger:int=32):
        self.detector = detector
        self.trigger = trigger
        self.CLICKED = False
    

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
                
                # USE OF RIGHT HAND STARTING TWO FINGERS
                elif 1 not in fingersL[3:] and 1 not in fingersR and 0 not in fingersL[1:3] and not self.CLICKED:
                    pyautogui.press("space")
                    print("KEY SPACE")
                    self.CLICKED = True
                
                # USE OF LEFT HAND STARTING TWO FINGERS
                elif 1 not in fingersR[3:] and 1 not in fingersL and 0 not in fingersR[1:3] and not self.CLICKED:
                    pyautogui.press("e")
                    print("KEY E(ACTION)")
                    self.CLICKED = True

        return frame
