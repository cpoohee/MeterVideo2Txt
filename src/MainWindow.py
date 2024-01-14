import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from VideoFeeder import VideoFeeder
from VideoScene import VideoScene
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

        rotate_none_action = QAction("No Rotation", self)
        rotate_none_action.setCheckable(True)
        rotate_none_action.setChecked(True)
        rotate_none_action.triggered.connect(self.no_rotation_video)

        rotate_c90_action = QAction("Rotate Clockwise 90" + u'\N{DEGREE SIGN}', self)
        rotate_c90_action.setCheckable(True)
        rotate_c90_action.triggered.connect(self.rotate_c90_video)

        rotate_180_action = QAction("Rotate 180" + u'\N{DEGREE SIGN}', self)
        rotate_180_action.setCheckable(True)
        rotate_180_action.triggered.connect(self.rotate_180_video)

        rotate_ac90_action = QAction("Rotate Anti-Clockwise 90" + u'\N{DEGREE SIGN}', self)
        rotate_ac90_action.setCheckable(True)
        rotate_ac90_action.triggered.connect(self.rotate_ac90_video)

        self.rotation_group = QActionGroup(self)
        self.rotation_group.addAction(rotate_none_action)
        self.rotation_group.addAction(rotate_c90_action)
        self.rotation_group.addAction(rotate_180_action)
        self.rotation_group.addAction(rotate_ac90_action)
        self.rotation_group.setExclusionPolicy(QActionGroup.ExclusionPolicy.Exclusive)
        self.rotation_group.setDisabled(True)

        self.orientation_menu.addAction(rotate_none_action)
        self.orientation_menu.addAction(rotate_c90_action)
        self.orientation_menu.addAction(rotate_180_action)
        self.orientation_menu.addAction(rotate_ac90_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("No Video Loaded.")

        # top widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Display video frames using VideoScene
        self.video_scene = VideoScene()
        view = QGraphicsView(self.video_scene)
        layout.addWidget(view, stretch = 10)
        self.video_scene.clicked_signal.connect(self.handle_poly_clicked)

        # slider stuff
        slider_widget = QWidget(self)
        slider_layout = QHBoxLayout()
        self.frame_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.frame_slider.setDisabled(True)
        self.frame_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.frame_slider.valueChanged.connect(self.update_slider_value)
        self.frame_slider.sliderReleased.connect(self.slider_released)
        slider_layout.addWidget(self.frame_slider)
        self.slider_label = QLabel("0", self)
        slider_layout.addWidget(self.slider_label)
        slider_widget.setLayout(slider_layout)

        layout.addWidget(slider_widget, stretch = 0)

        self.value_tracker_table = ValueTrackerQTable(1)
        layout.addWidget(self.value_tracker_table, stretch = 1)

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
            self.rotation_group.setEnabled(True)

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

    def update_slider_value(self, value):
        self.slider_label.setText(f'{value}')

    def slider_released(self):
        # to update video
        self.refresh_video()
        self.value_tracker_table.view_valuetracker(self.frame_slider.value())
        self.statusBar().showMessage(f'released at {self.frame_slider.value()}')

    def refresh_video(self):
        success, cv_img = self.feeder.grab_frame(self.frame_slider.value())
        pred = self.ocr.predict(cv_img)
        self.video_scene.update_screen(cv_img, pred)

    def no_rotation_video(self):
        self.feeder.set_rotate(None)
        self.refresh_video()

    def rotate_c90_video(self):
        self.feeder.set_rotate(VideoFeeder.ROTATE_90_CLOCKWISE)
        self.refresh_video()

    def rotate_180_video(self):
        self.feeder.set_rotate(VideoFeeder.ROTATE_180)
        self.refresh_video()

    def rotate_ac90_video(self):
        self.feeder.set_rotate(VideoFeeder.ROTATE_90_COUNTERCLOCKWISE)
        self.refresh_video()