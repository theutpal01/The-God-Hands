from threading import Thread
import cv2


class VideoGet:
    def __init__(self, win_size, src=0):
        self.stream = cv2.VideoCapture(src)
        cv2.namedWindow("Viewer", cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_AUTOSIZE)
        cv2.resizeWindow("Viewer", win_size[0], win_size[1])
        self.grabbed, self.frame = self.stream.read()
        self.stopped = False


    def start(self):
        Thread(target=self.get, args=()).start()
        return self
    

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                break
            else:
                self.grabbed, self.frame = self.stream.read()

    
    def showWin(self, frame):
        cv2.imshow("Viewer", frame)

