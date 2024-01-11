import numpy as np
from mmocr.apis import MMOCRInferencer

# ocr = MMOCRInferencer(det='MaskRCNN_IC15',
#                       rec='svtr-base')
# ocr('./data/pic.jpg', show=True, print_result=True)

# import mmcv
# import matplotlib.pyplot as plt
#
# predicted_img = mmcv.imread('./data/pic.jpg')
#
# plt.imshow(mmcv.bgr2rgb(predicted_img))
# plt.show()

class OCR:
    def __init__(self, det='MaskRCNN_IC15', rec='svtr-base'):
        """
        See https://mmocr.readthedocs.io/en/dev-1.x/modelzoo.html for model names
        :param det: Detection model. default as 'MaskRCNN_IC15'
        :param rec: Recognition model. default as 'svtr-base'
        """
        self.det = det
        self.rec = rec
        self.model = MMOCRInferencer(det=self.det, rec=self.rec)
    def predict(self, image_input:np.ndarray):
        """

        :param image_input: Image in numpy array. It should be in BGR order.
        :return: prediction dict
        """
        return self.model(image_input)