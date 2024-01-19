import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from VideoFeeder import VideoFeeder
from VideoScene import VideoScene, GraphicsViewWithMouse
from OCR import OCR
from ValueTracker import ValueTrackerQTable

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Meter Video To Text")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.orientation_menu = self.menu.addMenu("Orientation")

        # Load Video Action
        load_action = QAction("Load Video", self)
        load_action.triggered.connect(self.load_video)
        self.file_menu.addAction(load_action)

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        self.rotate_none_action = QAction("No Rotation", self)
        self.rotate_none_action.setCheckable(True)
        self.rotate_none_action.setChecked(True)
        self.rotate_none_action.triggered.connect(self.no_rotation_video)

        self.rotate_c90_action = QAction("Rotate Clockwise 90" + u'\N{DEGREE SIGN}', self)
        self.rotate_c90_action.setCheckable(True)
        self.rotate_c90_action.triggered.connect(self.rotate_c90_video)

        self.rotate_180_action = QAction("Rotate 180" + u'\N{DEGREE SIGN}', self)
        self.rotate_180_action.setCheckable(True)
        self.rotate_180_action.triggered.connect(self.rotate_180_video)

        self.rotate_ac90_action = QAction("Rotate Anti-Clockwise 90" + u'\N{DEGREE SIGN}', self)
        self.rotate_ac90_action.setCheckable(True)
        self.rotate_ac90_action.triggered.connect(self.rotate_ac90_video)

        self.rotation_group = QActionGroup(self)
        self.rotation_group.addAction(self.rotate_none_action)
        self.rotation_group.addAction(self.rotate_c90_action)
        self.rotation_group.addAction(self.rotate_180_action)
        self.rotation_group.addAction(self.rotate_ac90_action)
        self.rotation_group.setExclusionPolicy(QActionGroup.ExclusionPolicy.Exclusive)
        self.rotation_group.setDisabled(True)

        self.orientation_menu.addAction(self.rotate_none_action)
        self.orientation_menu.addAction(self.rotate_c90_action)
        self.orientation_menu.addAction(self.rotate_180_action)
        self.orientation_menu.addAction(self.rotate_ac90_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("No Video Loaded.")

        # top widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Display video frames using VideoScene
        self.video_scene = VideoScene()
        view = GraphicsViewWithMouse(self.video_scene)
        view.setMouseTracking(True)
        view.mouse_moved_signal.connect(self.handle_video_mousemove)
        layout.addWidget(view, stretch = 10)
        self.video_scene.clicked_signal.connect(self.handle_poly_clicked)

        # slider stuff
        slider_widget = QWidget(self)
        slider_layout = QHBoxLayout()
        self.slider_label = QLabel("frame:", self)
        self.slider_spinbox = QSpinBox(self)
        self.slider_spinbox.setDisabled(True)
        self.slider_spinbox.valueChanged.connect(self.spinbox_value_changed)
        slider_layout.addWidget(self.slider_label)
        slider_layout.addWidget(self.slider_spinbox)
        self.frame_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.frame_slider.setDisabled(True)
        self.frame_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.frame_slider.valueChanged.connect(self.update_slider_value)
        self.frame_slider.sliderReleased.connect(self.slider_released)
        slider_layout.addWidget(self.frame_slider)
        slider_widget.setLayout(slider_layout)
        layout.addWidget(slider_widget, stretch = 1)

        self.value_tracker_table = ValueTrackerQTable(1)
        layout.addWidget(self.value_tracker_table, stretch = 1)

        self.buttons_widget = QWidget(self)
        buttons_layout = QHBoxLayout()
        self.track_next_button = QPushButton("Track Next Frame")
        self.track_next_button.clicked.connect(self.track_next_button_clicked)
        self.track_subsequent_button = QPushButton("Track Subsequent Frames")
        self.track_subsequent_button.clicked.connect(self.track_subsequent_button_clicked)
        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_button_clicked)
        buttons_layout.addWidget(self.track_next_button)
        buttons_layout.addWidget(self.track_subsequent_button)
        buttons_layout.addWidget(self.export_button)
        self.buttons_widget.setLayout(buttons_layout)
        self.buttons_widget.setDisabled(True)
        layout.addWidget(self.buttons_widget)

        # finalise widget
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # # Window dimensions
        # geometry = self.screen().availableGeometry()
        # self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

        self.feeder = VideoFeeder()
        self.ocr = OCR()


    def load_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Load Video File", "",
                                                  "MPEG-4 (*.mp4);;AVI (*.avi)",
                                                  options=options)
        if fileName:
            self.statusBar().showMessage(fileName)
            self.feeder.set_video(fileName)
            self.frame_slider.setEnabled(True)
            self.frame_slider.setRange(0, self.feeder.max_frame() - 1)
            self.frame_slider.setTickPosition(0)
            self.slider_spinbox.blockSignals(True)
            self.slider_spinbox.setEnabled(True)
            self.slider_spinbox.setValue(0)
            self.slider_spinbox.setMaximum(self.feeder.max_frame() - 1)
            self.slider_spinbox.blockSignals(False)

            self.rotation_group.setEnabled(True)
            self.buttons_widget.setEnabled(True)

            self.value_tracker_table.reset_valuetracker_framesize(self.feeder.max_frame())

            self.slider_released()

    @pyqtSlot(str, float, float, float)
    def handle_poly_clicked(self, value, cx, cy, area):
        label, ok = QInputDialog().getText(self, "Enter Label Name:",
                                              "Label:", QLineEdit.Normal)
        if ok:
            if self.value_tracker_table.is_label_exists(label):
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Warning!")
                dlg.setText("Label already exists!")
                dlg.exec()
            else:
                self.value_tracker_table.add_label(label, cx, cy, area, value, self.frame_slider.value())
                self.value_tracker_table.view_valuetracker(self.frame_slider.value())

    def spinbox_value_changed(self, value):
        self.frame_slider.blockSignals(True)
        self.frame_slider.setValue(value)
        self.frame_slider.blockSignals(False)
        self.slider_released()

    def update_slider_value(self, value):
        self.slider_spinbox.blockSignals(True)
        self.slider_spinbox.setValue(value)
        self.slider_spinbox.blockSignals(False)

    def slider_released(self):
        # to update video
        _ = self.refresh_video()
        self.value_tracker_table.view_valuetracker(self.frame_slider.value())

        self.slider_spinbox.blockSignals(True)
        self.slider_spinbox.setValue(self.frame_slider.value())
        self.slider_spinbox.blockSignals(False)

        # self.statusBar().showMessage(f'released at {self.frame_slider.value()}')

    def handle_video_mousemove(self, x, y):
        self.statusBar().showMessage(f'Pixel {x:.0f}, {y:.0f}')

    def refresh_video(self):
        success, cv_img = self.feeder.grab_frame(self.frame_slider.value())
        pred = self.ocr.predict(cv_img)
        self.video_scene.update_screen(cv_img, pred)
        return pred

    def rotation_warning(self):
        dlg = QMessageBox(self)
        dlg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        dlg.setWindowTitle("Warning!")
        dlg.setText("Labels and predictions will be lost!")
        return dlg.exec()

    def reset_rotate_checkerbox(self):
        if self.feeder.get_rotate() == None:
            self.rotation_group.blockSignals(True)
            self.rotate_none_action.setChecked(True)
            self.rotation_group.blockSignals(False)

        if self.feeder.get_rotate() == VideoFeeder.ROTATE_90_CLOCKWISE:
            self.rotation_group.blockSignals(True)
            self.rotate_c90_action.setChecked(True)
            self.rotation_group.blockSignals(False)

        if self.feeder.get_rotate() == VideoFeeder.ROTATE_180:
            self.rotation_group.blockSignals(True)
            self.rotate_180_action.setChecked(True)
            self.rotation_group.blockSignals(False)

        if self.feeder.get_rotate() == VideoFeeder.ROTATE_90_COUNTERCLOCKWISE:
            self.rotation_group.blockSignals(True)
            self.rotate_ac90_action.setChecked(True)
            self.rotation_group.blockSignals(False)

    def no_rotation_video(self):
        # self.value_tracker_table.rotate_labels(self.feeder.get_rotate(), None)
        ret = self.rotation_warning()
        if ret == QMessageBox.Cancel:
            self.reset_rotate_checkerbox()
            return

        self.feeder.set_rotate(None)
        self.refresh_video()
        self.value_tracker_table.view_valuetracker(self.frame_slider.value())

    def rotate_c90_video(self):
        # self.value_tracker_table.rotate_labels(self.feeder.get_rotate(), VideoFeeder.ROTATE_90_CLOCKWISE)
        ret = self.rotation_warning()
        if ret == QMessageBox.Cancel:
            self.reset_rotate_checkerbox()
            return
        self.feeder.set_rotate(VideoFeeder.ROTATE_90_CLOCKWISE)
        self.refresh_video()
        self.value_tracker_table.view_valuetracker(self.frame_slider.value())

    def rotate_180_video(self):
        # self.value_tracker_table.rotate_labels(self.feeder.get_rotate(),
        #                                        VideoFeeder.ROTATE_180)
        ret = self.rotation_warning()
        if ret == QMessageBox.Cancel:
            self.reset_rotate_checkerbox()
            return
        self.feeder.set_rotate(VideoFeeder.ROTATE_180)
        self.refresh_video()
        self.value_tracker_table.view_valuetracker(self.frame_slider.value())

    def rotate_ac90_video(self):
        # self.value_tracker_table.rotate_labels(self.feeder.get_rotate(),
        #                                        VideoFeeder.ROTATE_90_COUNTERCLOCKWISE)
        ret = self.rotation_warning()
        if ret == QMessageBox.Cancel:
            self.reset_rotate_checkerbox()
            return
        self.feeder.set_rotate(VideoFeeder.ROTATE_90_COUNTERCLOCKWISE)
        self.refresh_video()
        self.value_tracker_table.view_valuetracker(self.frame_slider.value())

    def track_next_button_clicked(self):
        if self.frame_slider.value() < self.feeder.max_frame() - 1:
            self.frame_slider.setValue(self.frame_slider.value() + 1)
            pred = self.refresh_video()
            # do filtering in value tracker and add at value + 1
            self.value_tracker_table.track_labels(pred, self.frame_slider.value())
            # by now, new values shd be updated in the value tracker
            self.value_tracker_table.view_valuetracker(self.frame_slider.value())

    def track_subsequent_button_clicked(self):
        progress = QProgressDialog("Tracking subsequent frames...", "Abort", self.frame_slider.value(), self.feeder.max_frame(), self);
        progress.setWindowModality(Qt.WindowModal)
        while self.frame_slider.value() < self.feeder.max_frame() - 1:
            self.track_next_button_clicked()
            progress.setValue(self.frame_slider.value())
            if progress.wasCanceled():
                break
        progress.close()

    def export_button_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fd = QFileDialog(self, "Export File", "",
                                       options=options)

        filters = ["CSV File(*.csv)",
                   "Excel File(*.xlsx)",
                   "Pickle File(*.pkl)"]
        fd.setNameFilters(filters)
        fd.setAcceptMode(QFileDialog.AcceptSave)

        if fd.exec():
            filename = fd.selectedFiles()[0]
            format = fd.selectedNameFilter()

            if filename:
                filepath = Path(filename)
                # strip extensions
                filepath.with_suffix('')

                if format=='CSV File(*.csv)':
                    format='.csv'
                elif format=='Excel File(*.xlsx)':
                    format='.xlsx'
                elif format=='Pickle File(*.pkl)':
                    format='.pkl'
                filename = str(filepath.with_suffix(format))
                # check manually for override, built in file dialog does not check selected filter extension
                if QFile.exists(filename):
                    qm = QMessageBox()
                    qm.question(self, '',
                                f"{QFileInfo(filename).fileName()} already exists.\n Do you want to replace it?",
                                qm.Yes | qm.No)
                    if qm.No:
                        return
                self.value_tracker_table.export_values(filename, format)
                self.statusBar().showMessage(f'Saved to: {filename:}')
