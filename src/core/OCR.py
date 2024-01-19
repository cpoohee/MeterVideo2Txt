import os
import numpy as np
from mmocr.apis import TextDetInferencer, TextRecInferencer
from mmocr.utils import bbox2poly, crop_img, poly2bbox
# from mmocr.apis import MMOCRInferencer
from pathlib import Path
import wget
from src.core.ocr_models import det_models, rec_models, models, models_url, model_config

class OCR:
    def __init__(self, det='MaskRCNN_IC15', rec='svtr-base'):
        """
        See https://mmocr.readthedocs.io/en/dev-1.x/modelzoo.html for model names
        :param det: Detection model. default as 'MaskRCNN_IC15'
        :param rec: Recognition model. default as 'svtr-base'
        """
        self.det = det
        self.rec = rec

        # there is an issue if detected polygons with invalid sized, resulting in crash.
        # see https://github.com/open-mmlab/mmocr/issues/1886
        # self.model = MMOCRInferencer(det=self.det, rec=self.rec)

        # let's resort to Standard Inferencer

        if det is not None:
            self.set_detector(self.det)

        if rec is not None:
            self.set_recognizer(self.rec)
    def set_detector(self, det='MaskRCNN_IC15'):
        if det == 'Fixed Area':
            self.detector = None
        else:
            if not self.check_model_exists(det):
                self.download_model(det)
            self.detector = TextDetInferencer(weights=models[det])

    def set_recognizer(self, rec='svtr-base'):
        if not self.check_model_exists(rec):
            self.download_model(rec)
        self.recognizer = TextRecInferencer(model=model_config[rec], weights=models[rec])

    def check_model_exists(self, model_name):
        if model_name == 'Fixed Area':
            return True
        cur_dir = Path(os.getcwd())
        det_model_path = cur_dir / Path(models[model_name])
        return det_model_path.exists()

    def download_model(self, model_name):
        if model_name == 'Fixed Area':
            return True
        cur_dir = Path(os.getcwd())
        model_path = cur_dir / Path(models[model_name])
        try:
            wget.download(models_url[model_name], model_path.as_posix())
            return True
        except:
            return False

    def predict(self, image_input:np.ndarray):
        """

        :param image_input: Image in numpy array. It should be in BGR order.
        :return: prediction dict
        """

        # using MMOCRInferencer
        # return self.model(image_input)

        # using Standard Inferencer
        result = {}
        result['det'] = self.detector(image_input,
                                      return_datasamples=True)['predictions']

        result['valid_polys'] = [] # extra work to filter valid polygons

        # extract image from polygons
        result['rec'] = []
        det_pred = result['det'][0].pred_instances
        self.rec_inputs = []
        for polygon in det_pred['polygons']:
            # Roughly convert the polygon to a quadangle with
            # 4 points
            quad = bbox2poly(poly2bbox(polygon)).tolist()
            c_img = crop_img(image_input, quad)
            # check valid img, ignore if width or length is zero
            if c_img.shape[0] > 0 and c_img.shape[1] > 0:
                self.rec_inputs.append(c_img)
                result['valid_polys'].append(polygon)

        if self.rec_inputs:
            result['rec'].append(
                self.recognizer(
                    self.rec_inputs,
                    return_datasamples=True,)['predictions'])

        # format the prediction dict similar to MMOCRInferencer's output
        pred = {}
        inner_pred = {}
        rec_texts = []
        for rec_res in result['rec'][0]:
            rec_texts.append(rec_res.pred_text.item)
        inner_pred['rec_texts'] = rec_texts

        inner_pred['det_polygons'] = result['valid_polys']

        pred['predictions'] = [inner_pred]

        return pred

    def recognize_bboxes(self, image_input:np.ndarray, bboxes):
        pass
