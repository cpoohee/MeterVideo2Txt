import mmcv
import matplotlib.pyplot as plt
from VideoFeeder import VideoFeeder
def main():
    feeder = VideoFeeder()
    feeder.set_video('./data/vid.mp4')
    feeder.set_rotate(VideoFeeder.ROTATE_90_COUNTERCLOCKWISE)

    print(feeder.frame_count)
    print(feeder.fps)

    success, image = feeder.grab_frame(1)

    plt.imshow(mmcv.bgr2rgb(image))
    plt.show()

if __name__=="__main__":
    main()