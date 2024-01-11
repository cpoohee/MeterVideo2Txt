import torch
import mmcv
import matplotlib.pyplot as plt
from VideoFeeder import VideoFeeder
from OCR import OCR
from WordMatch import WordMatch

def main():
    # feeder = VideoFeeder()
    # feeder.set_video('./data/vid.mp4')
    # feeder.set_rotate(VideoFeeder.ROTATE_90_COUNTERCLOCKWISE)
    #
    # print(feeder.frame_count)
    # print(feeder.fps)
    #
    # success, image = feeder.grab_frame(1)
    #
    # ocr = OCR()
    #
    # res = ocr.predict(image)

    # print(res['det_ploygons'])

    # plt.imshow(mmcv.bgr2rgb(image))
    # plt.show()

    word_match = WordMatch()
    word_match.add_keyword('sp02')
    word_match.add_keyword('PRbpm')

    print(word_match.match_to_keyword('spO2'))
    print(word_match.match_to_keyword('bpm'))


if __name__=="__main__":
    main()