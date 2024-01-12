from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem
from PyQt5.QtGui import QBrush, QPen, QPixmap, QImage
from PyQt5.QtCore import Qt

class VideoScene(QGraphicsScene):
    def __init__(self):
        super(VideoScene, self).__init__()
        self.pic = QGraphicsPixmapItem()
        self.pic.setPixmap(QPixmap())
        self.addItem(self.pic)

        # rect = QGraphicsRectItem(0, 0, 200, 50)
        #
        # # Set the origin (position) of the rectangle in the scene.
        # rect.setPos(50, 20)
        #
        # # Define the brush (fill).
        # brush = QBrush(Qt.red)
        # rect.setBrush(brush)
        #
        # # Define the pen (line)
        # pen = QPen(Qt.cyan)
        # pen.setWidth(10)
        # rect.setPen(pen)
        #
        # brush = QBrush(Qt.blue)
        #
        # pen = QPen(Qt.green)
        # pen.setWidth(5)
        #
        # # Add the items to the scene. Items are stacked in the order they are added.
        # self.addItem(rect)
    def update_pixmap(self, pixmap):
        self.pic.setPixmap(pixmap)

    def update_cvImg(self, cv_img):
        self.convert_cv_img_to_QtImage(cv_img)
        pixmap = self.convert_cv_img_to_QtImage(cv_img)
        self.update_pixmap(pixmap)

    def convert_cv_img_to_QtImage(self, cv_img):
        image = QImage(cv_img, cv_img.shape[1], cv_img.shape[0], cv_img.shape[1] * 3, QImage.Format_BGR888)
        return QPixmap(image)