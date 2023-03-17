from VideoGet import VideoGet
from HandDetection import HandDetection
from Gestures.Controller import Controller
from Gestures.MouseGestures import MouseGestures
from Gestures.KeyboardGestures import KeyboardGestures
from Gestures.GamingGestures import GamingGestures
import cv2, time, pyautogui

WIN_NAME = "The God Hands (The Invisible Hands v2.O)"
FRAME_SIZE = (700, 500)
FRAME_MARGIN = (50, 110, 200, 110)                # NESW FORMAT
pyautogui.FAILSAFE = False

def addTextOnScreen(frame, text, coordinates, color, font, font_scale, thickness):
    cv2.putText(frame, text, coordinates, font, font_scale, color, thickness)
    return frame


def Viewer(src = 0):
    video_gettr = VideoGet(FRAME_SIZE, src)
    detector = HandDetection(2)
    pTime = 0
    statusText = "Hello"

    # GESTURES INITIALIZED
    control = Controller(detector)
    control.setForMouse()
    mouseGest = MouseGestures(detector, 30, 20)
    keyboardGest = KeyboardGestures(detector, 23)
    gamingGest = GamingGestures(detector, 23)

    while True:

        # CAPTURING IMAGES
        video_gettr.get()

        # PROGRAM QUIT CONDITIONS
        if cv2.waitKey(1) == 27:
            break

        # GET FRAME AT EACH ITERATION
        frame = video_gettr.frame
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, FRAME_SIZE)

        # GET FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        
        # DISPLAY FPS ON THE SCREEN
        frame = addTextOnScreen(frame, f"FPS: {int(fps)}", (6, 30), (220, 219, 0), cv2.FONT_HERSHEY_DUPLEX, 0.9, 1)
        

        # MAIN TASKS
        statusText = control.getStatus()
        hands, frame = detector.findHands(frame)
        frame = control.detectGesture(frame, hands)


        if statusText == "Mouse": frame = mouseGest.detectMovements(FRAME_SIZE, FRAME_MARGIN, frame, hands)
        elif statusText == "Keyboard": frame = keyboardGest.detectGestures(frame, hands)
        elif statusText == "Gaming": frame = gamingGest.detectGestures(frame, hands)
        

        # SHOWING THE FRAME AND STATUS ON THE SCREEN
        addTextOnScreen(frame, "Active: " + statusText + " Mode", (5, FRAME_SIZE[1] - 10), (180, 225, 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, 1)
        video_gettr.showWin(frame)
        statusText = ""


    video_gettr.stream.release()
    cv2.destroyAllWindows()


def main():
    Viewer(0)
    


if __name__ == '__main__':
    main()