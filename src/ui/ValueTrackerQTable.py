from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
from src.core.ValueTracker import ValueTracker

class ValueTrackerQTable(QTableWidget):
    def __init__(self, frame_size):
        super(QTableWidget, self).__init__()
        self.valuetracker = ValueTracker(frame_size)
        self.headers = ["label", "x", "y", "value"]
        # self.headers = ["label", "x", "y", "area", "value"]
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.view_valuetracker(0)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def reset_valuetracker_framesize(self, frame_size):
        self.valuetracker = ValueTracker(frame_size)
        self.view_valuetracker(0)

    def is_label_exists(self, label):
        return self.valuetracker.label_exists(label)

    def add_label(self, label, cx, cy, area, value, frame_i):
        self.valuetracker.add_label(label, cx, cy, area, value, frame_i)

    def track_labels(self, pred, frame_i):
        self.valuetracker.track_labels(pred, frame_i)

    def view_valuetracker(self, frame_i):
        self.clearContents()
        frame_info = self.valuetracker.get_frame_info(frame_i)
        data = {}
        for self.header in self.headers:
            data[self.header] = []

        for key in frame_info.keys():
            data["label"].append(key)
            cx, cy, area, value = frame_info[key]
            data["x"].append(int(cx)) # to int
            data["y"].append(int(cy)) # to int
            # data["area"].append(area)
            data["value"].append(value)

        self.setRowCount(len(data["label"]))
        for n, key in enumerate(self.headers):
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(str(item))
                self.setItem(m, n, newitem)

        self.resizeRowsToContents()

    def export_values(self, filename, format):
        self.valuetracker.export_values(filename, format)