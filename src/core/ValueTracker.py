import math
import numpy as np

from PyQt5.QtGui import QPolygonF
from PyQt5.QtCore import QPointF
import pandas as pd

class ValueTracker:
    def __init__(self, frame_size):
        self.frame = [dict() for _ in range(frame_size)]
        self.labels = set()

    def add_label(self, label, cx, cy, area, value, frame_i):
        if label not in self.labels:
            self.labels.add(label)
            self.frame[frame_i][label] = (cx, cy, area, value)

    def label_exists(self, label):
        return label in self.labels

    def track_labels(self, pred, frame_i):
        if pred is None:
            return
        # process into qpolygons
        pred = pred['predictions'][0]
        pred_value_list = pred['rec_texts']
        pred_poly_list = pred['det_polygons']
        qpoly_list = [] # (Cx, Cy, area)

        for pred_poly in pred_poly_list:
            qpoly = self.get_polygon(pred_poly)
            qpoly_list.append(self.get_centroid_poly(qpoly))

        # probably can be optimised for efficiency in future
        for label in self.labels:
            # search previous available prediction
            i = frame_i - 1
            while i >= 0:
                if label in self.frame[i]:
                    prev_cx, prev_cy, prev_area, prev_value = self.frame[i][label]
                    break
                else:
                    i = i - 1
            if i == -1:
                continue
            else:
                # find nearest point match in pred
                min_dist_idx = self.nearest_point(prev_cx, prev_cy, qpoly_list)
                # assign match
                new_cx, new_cy, new_area = qpoly_list[min_dist_idx]
                self.frame[frame_i][label] = (new_cx, new_cy, new_area, pred_value_list[min_dist_idx])
                # may use area as matching criteria next time

    def nearest_point(self, cx, cy, points):
        ref_point = [cx, cy]
        min_dist = np.finfo(np.float64).max
        min_dist_idx = None
        for i, point in enumerate(points):
            cur_point = [ point[0], point[1]]
            dist = math.dist(ref_point, cur_point)
            if dist < min_dist:
                min_dist = dist
                min_dist_idx = i

        return min_dist_idx

    def get_polygon(self, polys):
        qpoly = QPolygonF()
        list_y = polys[1::2]
        list_x = polys[::2]
        for x, y in zip(list_x, list_y):
            qpoly.append(QPointF(x, y))
        return qpoly

    def get_centroid_poly(self, polygon):
        N = polygon.size()
        # minimal sanity check
        if N < 3:
            raise ValueError('At least 3 vertices must be passed.')
        sum_A, sum_Cx, sum_Cy = 0, 0, 0
        last_iteration = N - 1
        # from 0 to N-1
        for i in range(N):
            if i != last_iteration:
                shoelace = polygon[i].x() * polygon[i + 1].y() - polygon[i + 1].x() * polygon[i].y()
                sum_A += shoelace
                sum_Cx += (polygon[i].x() + polygon[i + 1].x()) * shoelace
                sum_Cy += (polygon[i].y() + polygon[i + 1].y()) * shoelace
            else:
                # N-1 case (last iteration): substitute i+1 -> 0
                shoelace = polygon[i].x() * polygon[0].y() - polygon[0].x() * polygon[i].y()
                sum_A += shoelace
                sum_Cx += (polygon[i].x() + polygon[0].x()) * shoelace
                sum_Cy += (polygon[i].y() + polygon[0].y()) * shoelace
        A = 0.5 * sum_A
        factor = 1 / (6 * A)
        Cx = factor * sum_Cx
        Cy = factor * sum_Cy
        # returning abs of A is the only difference to
        # the algo from above link
        return Cx, Cy, abs(A)

    def update_label_info(self, label, cx, cy, area, value, frame_i):
        if label in self.labels:
            self.frame[frame_i][label] = (cx, cy, area, value)

    def get_frame_info(self, frame_i):
        return self.frame[frame_i]

    def export_values(self, filename, format='.csv'):
        data = []
        data_col = ['frameNumber', 'label', 'value']
        for lab in self.labels:
            for f_number, frame in enumerate(self.frame):
                if lab in frame:
                    _, _, _, value = frame[lab]
                    data.append([f_number, lab, value])

        df = pd.DataFrame(data, columns = data_col)

        if format=='.csv':
            df.to_csv(filename, index=False)
        elif format=='.xlsx':
            df.to_excel(filename, index=False)
        elif format=='pkl':
            df.to_pickle(filename, index=False)
