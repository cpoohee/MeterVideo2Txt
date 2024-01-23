import numpy as np
import cv2

class VideoFeeder:
    """
    Reads video frames into image. Wrapper to openCV video Capture.
    """
    ROTATE_90_CLOCKWISE = cv2.ROTATE_90_CLOCKWISE
    ROTATE_180 = cv2.ROTATE_180
    ROTATE_90_COUNTERCLOCKWISE = cv2.ROTATE_90_COUNTERCLOCKWISE
    def __init__(self):
        self.cap = None
        self.frame_count = None
        self.fps = None
        self.rotate = None

    def set_video(self, video_input:str):
        self.cap = cv2.VideoCapture(video_input)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

    def close_video(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.frame_count = None
        self.fps = None
        self.rotate = None

    def set_rotate(self, rotate):
        """

        :param rotate: One of [ROTATE_90_CLOCKWISE, ROTATE_180, ROTATE_90_COUNTERCLOCKWISE, None]
        """
        self.rotate = rotate
    def get_rotate(self):
        return self.rotate

    def grab_frame(self, frame:int ) -> tuple([bool, np.ndarray]):
        """
        Reads target frame from video.
        :param frame: integer frame value
        :return: success(bool), image (in numpy.ndarray BGR)
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        success, image = self.cap.read()

        if self.rotate is not None:
            image = cv2.rotate(image, self.rotate)

        return success, image

    def fps(self):
        return self.fps
    def max_frame(self):
        return self.frame_count