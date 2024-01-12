from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem, \
    QGraphicsPolygonItem
from PyQt5.QtGui import QBrush, QPen, QPixmap, QImage, QPolygonF
from PyQt5.QtCore import Qt, QPointF

class QGraphicsPolygonItemHovers (QGraphicsPolygonItem):
    def __init__(self,parent=None):
        super(QGraphicsPolygonItemHovers, self).__init__(parent)
        self.setAcceptHoverEvents(True)
        self.text = ""

    def setText(self, text):
        self.text = text
    def hoverEnterEvent(self, event):
        self.setToolTip(self.text)

class VideoScene(QGraphicsScene):
    def __init__(self):
        super(VideoScene, self).__init__()
        pic = QGraphicsPixmapItem()
        pic.setPixmap(QPixmap())
        self.addItem(pic)

    def update_pixmap(self, pixmap):
        pic = QGraphicsPixmapItem()
        pic.setPixmap(pixmap)
        self.addItem(pic)

    def update_cvImg(self, cv_img):
        self.convert_cv_img_to_QtImage(cv_img)
        pixmap = self.convert_cv_img_to_QtImage(cv_img)
        self.update_pixmap(pixmap)

    def update_screen(self, cv_img, pred=None):
        self.clear()
        self.update_cvImg(cv_img)

        # draw bounding boxes if there is stuff
        if pred is not None:
            pred = pred['predictions'][0]
            pred_text_list = pred['rec_texts']
            pred_poly_list = pred['det_polygons']
            for idx, pred_word in enumerate(pred_text_list):
                qpoly = self.get_polygon(pred_poly_list[idx])
                poly_item = QGraphicsPolygonItemHovers(qpoly)
                poly_item.setText(pred_word)
                # poly_item.setBrush(QBrush(Qt.yellow))
                pen = QPen(Qt.yellow)
                pen.setWidth(10)
                poly_item.setPen(pen)
                self.addItem(poly_item)

    def get_polygon(self, polys):
        qpoly = QPolygonF()
        listY = polys[1::2]
        listX = polys[::2]
        for x, y in zip(listX, listY):
            qpoly.append(QPointF(x, y))
        return qpoly

    def convert_cv_img_to_QtImage(self, cv_img):
        image = QImage(cv_img, cv_img.shape[1], cv_img.shape[0], cv_img.shape[1] * 3, QImage.Format_BGR888)
        return QPixmap(image)

    def print_label(text):
        print(text)


