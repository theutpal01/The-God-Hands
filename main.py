from VideoGet import VideoGet
from HandDetection import HandDetection
from Gestures.MouseGestures import MouseGestures
from Gestures.KeyboardGestures import KeyboardGestures
from Gestures.GamingGestures import GamingGestures
import cv2
import time, pyautogui
import numpy as np

FRAME_SIZE = (pyautogui.size()[0] - 400, pyautogui.size()[1] - 200)
FRAME_MARGIN = (50, 200, 200, 200)
pyautogui.FAILSAFE = False

def addTextOnScreen(frame, text, coordinates, color, font, font_scale, thickness):
    cv2.putText(frame, text, coordinates, font, font_scale, color, thickness)
    return frame


def threadVideoGet(src = 0):
    video_gettr = VideoGet(FRAME_SIZE, src).start()
    detector = HandDetection(2)
    pTime = 0
    statusText = "Hello"

    # GESTURES
    mouseGest = MouseGestures(detector, 33, 11)
    keyboardGest = KeyboardGestures(detector, 33)
    gamingGest = GamingGestures(detector, 33)

    while True:
        # PROGRAM QUIT CONDITIONS
        if cv2.waitKey(1) == 27 or video_gettr.stopped:
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
        hands, frame = detector.findHands(frame)
        # frame = mouseGest.detectMovements(FRAME_SIZE, FRAME_MARGIN, frame, hands)
        frame = keyboardGest.detectGestures(frame, hands, 50)
        # frame = gamingGest.detectGestures(frame, hands)
        

        # SHOWING THE FRAME AND STATUS ON THE SCREEN
        addTextOnScreen(frame, statusText, (5, FRAME_SIZE[1] - 10), (225, 0, 225,), cv2.FONT_HERSHEY_DUPLEX, 0.8, 1)
        video_gettr.showWin(frame)
        statusText = ""


    video_gettr.stream.release()
    cv2.destroyAllWindows()


def main():
    threadVideoGet(0)
    
    

if __name__ == '__main__':
    main()