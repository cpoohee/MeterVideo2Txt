from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
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

    def update_label_info(self, label, cx, cy, area, value, frame_i):
        if label in self.labels:
            self.frame[frame_i][label] = (cx, cy, area, value)

    def get_frame_info(self, frame_i):
        return self.frame[frame_i]


class ValueTrackerQTable(QTableWidget):
    def __init__(self, frame_size):
        super(QTableWidget, self).__init__()
        self.valuetracker = ValueTracker(frame_size)
        self.headers = ["label", "x", "y", "area", "value"]
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.view_valuetracker(0)

    def reset_valuetracker_framesize(self, frame_size):
        self.valuetracker = ValueTracker(frame_size)
        self.view_valuetracker(0)

    def is_label_exists(self, label):
        return self.valuetracker.label_exists(label)

    def add_label(self, label, cx, cy, area, value, frame_i):
        self.valuetracker.add_label(label, cx, cy, area, value, frame_i)

    def view_valuetracker(self, frame_i):
        self.clearContents()
        frame_info = self.valuetracker.get_frame_info(frame_i)
        data = {}
        for self.header in self.headers:
            data[self.header] = []

        for key in frame_info.keys():
            data["label"].append(key)
            cx, cy, area, value = frame_info[key]
            data["x"].append(cx)
            data["y"].append(cy)
            data["area"].append(area)
            data["value"].append(value)

        self.setRowCount(len(data["label"]))
        for n, key in enumerate(self.headers):
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(str(item))
                self.setItem(m, n, newitem)

        self.resizeRowsToContents()
