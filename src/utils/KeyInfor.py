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
        list_y = poly_list[1::2]
        list_x = poly_list[::2]
        cx, cy, _ = self.centroid_poly(list_x, list_y)
        return int(cx), int(cy)

    def centroid_poly(self, X, Y):
        """https://en.wikipedia.org/wiki/Centroid#Of_a_polygon"""
        N = len(X)
        # minimal sanity check
        if not (N == len(Y)):
            raise ValueError('X and Y must be same length.')
        elif N < 3:
            raise ValueError('At least 3 vertices must be passed.')
        sum_A, sum_Cx, sum_Cy = 0, 0, 0
        last_iteration = N - 1
        # from 0 to N-1
        for i in range(N):
            if i != last_iteration:
                shoelace = X[i] * Y[i + 1] - X[i + 1] * Y[i]
                sum_A += shoelace
                sum_Cx += (X[i] + X[i + 1]) * shoelace
                sum_Cy += (Y[i] + Y[i + 1]) * shoelace
            else:
                # N-1 case (last iteration): substitute i+1 -> 0
                shoelace = X[i] * Y[0] - X[0] * Y[i]
                sum_A += shoelace
                sum_Cx += (X[i] + X[0]) * shoelace
                sum_Cy += (Y[i] + Y[0]) * shoelace
        A = 0.5 * sum_A
        factor = 1 / (6 * A)
        Cx = factor * sum_Cx
        Cy = factor * sum_Cy
        # returning abs of A is the only difference to
        # the algo from above link
        return Cx, Cy, abs(A)