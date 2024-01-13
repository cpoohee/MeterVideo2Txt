from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, \
    QGraphicsPolygonItem
from PyQt5.QtGui import QPen, QPixmap, QImage, QPolygonF
from PyQt5.QtCore import Qt, QPointF, pyqtSignal, pyqtSlot

class QGraphicsPolygonItemHovers (QGraphicsPolygonItem):
    def __init__(self,parent=None):
        super(QGraphicsPolygonItemHovers, self).__init__(parent)
        self.setAcceptHoverEvents(True)
        self.text = ""
        self.set_unhighlighted()

    def setText(self, text):
        self.text = text

    def hoverEnterEvent(self, event):
        self.setToolTip(self.text)
        self.set_highlighted()

    def hoverLeaveEvent(self, event):
        self.set_unhighlighted()

    def mousePressEvent(self, event, QGraphicsSceneMouseEvent=None):
        if event.button() == Qt.LeftButton:
            cx, cy, area = self.get_centroid_poly()
            self.scene().clicked_signal.emit(self.text, cx, cy, area)

    def set_highlighted(self):
        pen = QPen(Qt.yellow)
        pen.setWidth(10)
        self.setPen(pen)
        self.update()

    def set_unhighlighted(self):
        pen = QPen(Qt.white)
        pen.setWidth(3)
        self.setPen(pen)
        self.update()

    def get_centroid_poly(self):
        """https://en.wikipedia.org/wiki/Centroid#Of_a_polygon"""
        N = self.polygon().size()
        # minimal sanity check
        if N < 3:
            raise ValueError('At least 3 vertices must be passed.')
        sum_A, sum_Cx, sum_Cy = 0, 0, 0
        last_iteration = N - 1
        # from 0 to N-1
        for i in range(N):
            if i != last_iteration:
                shoelace = self.polygon()[i].x() * self.polygon()[i + 1].y() - self.polygon()[i + 1].x() * self.polygon()[i].y()
                sum_A += shoelace
                sum_Cx += (self.polygon()[i].x() + self.polygon()[i + 1].x()) * shoelace
                sum_Cy += (self.polygon()[i].y() + self.polygon()[i + 1].y()) * shoelace
            else:
                # N-1 case (last iteration): substitute i+1 -> 0
                shoelace = self.polygon()[i].x() * self.polygon()[0].y() - self.polygon()[0].x() * self.polygon()[i].y()
                sum_A += shoelace
                sum_Cx += (self.polygon()[i].x() + self.polygon()[0].x()) * shoelace
                sum_Cy += (self.polygon()[i].y() + self.polygon()[0].y()) * shoelace
        A = 0.5 * sum_A
        factor = 1 / (6 * A)
        Cx = factor * sum_Cx
        Cy = factor * sum_Cy
        # returning abs of A is the only difference to
        # the algo from above link
        return Cx, Cy, abs(A)

class VideoScene(QGraphicsScene):
    clicked_signal = pyqtSignal(str, float, float , float, name='clicked_signal')
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
        self.convert_cv_img_to_qtimage(cv_img)
        pixmap = self.convert_cv_img_to_qtimage(cv_img)
        self.update_pixmap(pixmap)

    def update_screen(self, cv_img, pred=None):
        self.clear()
        self.update_cvImg(cv_img)
        self.setSceneRect(0,0, cv_img.shape[1], cv_img.shape[0])

        # draw bounding boxes if there is stuff
        if pred is not None:
            pred = pred['predictions'][0]
            pred_text_list = pred['rec_texts']
            pred_poly_list = pred['det_polygons']
            for idx, pred_word in enumerate(pred_text_list):
                qpoly = self.get_polygon(pred_poly_list[idx])
                poly_item = QGraphicsPolygonItemHovers(qpoly)
                poly_item.setText(pred_word)
                self.addItem(poly_item)
            # self.clicked_signal.connect(self.handle_poly_clicked)

    def get_polygon(self, polys):
        qpoly = QPolygonF()
        list_y = polys[1::2]
        list_x = polys[::2]
        for x, y in zip(list_x, list_y):
            qpoly.append(QPointF(x, y))
        return qpoly

    def convert_cv_img_to_qtimage(self, cv_img):
        image = QImage(cv_img, cv_img.shape[1], cv_img.shape[0], cv_img.shape[1] * 3, QImage.Format_BGR888)
        return QPixmap(image)
