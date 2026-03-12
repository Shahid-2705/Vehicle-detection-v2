import cv2

class VideoCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

    def get_frame(self):
        success, frame = self.cap.read()
        if success:
            _, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        return None
