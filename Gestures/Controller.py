from HandDetection import HandDetection


class Controller:
    def __init__(self, detector:HandDetection):
        self.Mouse = None
        self.Keyboard = None
        self.Gaming = None
        self.detector = detector

    
    def detectGesture(self, frame, hands):

        if len(hands) == 2:
            handL, handR = None, None
            handL = hands[0] if hands[0].get("type") == "Left" else hands[1]
            handR = hands[0] if hands[0].get("type") == "Right" else hands[1]

            fingersL, handInfoL = self.detector.fingersUpAndHandSide(handL)
            fingersR, handInfoR = self.detector.fingersUpAndHandSide(handR)

            if handInfoL[0][:-1] == "Front" == handInfoR[0][:-1] and handInfoL[1][:-1] == "Up" == handInfoR[1][:-1]:

                if 1 not in fingersL[2:4] and 1 not in fingersR[2:4] and fingersL[1] == fingersL[4] == 1 == fingersR[1] == fingersR[4]:
                    dist, _, frame = self.detector.findDistance(handL.get("center"), handR.get("center"), frame)

                    if dist < 220:
                        self.setForMouse()

                    elif 220 < dist < 330:
                        self.setForKeyboard()

                    elif dist > 330:
                        self.setForGaming()

        return frame

    
    def getStatus(self):
        if self.Mouse:
            return "Mouse"
        elif self.Keyboard:
            return "Keyboard"
        elif self.Gaming:
            return "Gaming"


    def setForMouse(self):
        self.Mouse = True
        self.Keyboard = False
        self.Gaming = False
        print("Active: Mouse")

    
    def setForKeyboard(self):
        self.Keyboard = True
        self.Mouse = False
        self.Gaming = False
        print("Active: Keyboard")

    
    def setForGaming(self):
        self.Gaming = True
        self.Mouse = False
        self.Keyboard = False
        print("Active: Gaming")
