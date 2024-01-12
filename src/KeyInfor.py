import numpy as np
from WordMatch import WordMatch
class KeyInfor:
    """
    Parses OCR extracted text and returns predicted Key Information.
    Uses historical position of keywords to heuristically predict expected word locations.
    """
    def __init__(self):
        self.word_match = WordMatch()

    def add_keyword(self, word):
        self.word_match.add_keyword(word)

    def remove_keyword(self, word):
        self.word_match.remove_keyword(word)

    def parse_ocr(self, ocr_pred, threshold=0.9):
        pred = ocr_pred['predictions'][0]
        pred_text_list = pred['rec_texts']
        pred_poly_list = pred['det_polygons']

        interest_word = []
        interest_word_score = []
        original_word = []
        interest_word_center = []

        for idx, pred_word in enumerate(pred_text_list):
            clean_word = pred_word.replace('<UKN>', '')
            matched_word, matched_score = self.word_match.match_to_keyword(clean_word, threshold)
            if matched_word is not None:
                xc, yc = self.polygon_center(pred_poly_list[idx])
                interest_word.append(matched_word)
                interest_word_center.append([xc, yc])
                original_word.append(pred_word)
                interest_word_score.append(matched_score)

        return interest_word, interest_word_center, original_word, interest_word_score

    def polygon_center(self, poly_list):
        listY = poly_list[1::2]
        listX = poly_list[::2]
        xbar = np.mean(listX)
        ybar = np.mean(listY)
        return int(xbar), int(ybar)