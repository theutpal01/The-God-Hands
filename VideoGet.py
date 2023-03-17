import cv2


class VideoGet:
    def __init__(self, win_size, src=0):
        self.stream = cv2.VideoCapture(src)
        cv2.namedWindow("The Invisible Hands", cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_AUTOSIZE)
        cv2.resizeWindow("The Invisible Hands", win_size[0], win_size[1])
        self.grabbed, self.frame = self.stream.read()


    def get(self):
        self.grabbed, self.frame = self.stream.read()

    
    def showWin(self, frame):
        cv2.imshow("The Invisible Hands", frame)

