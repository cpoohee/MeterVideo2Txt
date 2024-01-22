from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, \
    QGraphicsPolygonItem, QGraphicsView, QRubberBand, QGraphicsRectItem
from PyQt5.QtGui import QPen, QPixmap, QImage, QPolygonF
from PyQt5.QtCore import Qt, QPointF, pyqtSignal, QRect, QSize, QObject, pyqtSlot
from src.utils.geometry import get_centroid_poly

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
            cx, cy, area = get_centroid_poly(self.polygon())
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

class FixedBoxes(QObject):
    def __init__(self):
        super(QObject).__init__()
        self.boxes = []
        self.poly_items = []  # reuse existing polygon items in scene for display

    def clear_boxes(self):
        self.boxes.clear()
        self.poly_items.clear()

    def add_box(self, box:QPolygonF):
        self.boxes.append(box)
        poly = QGraphicsPolygonItemHovers(box)
        self.poly_items.append(poly)

    def get_boxes(self):
        """
        Bounding boxes for recognisers
        """
        return self.boxes

    def get_polygons_items(self):
        """
        For drawing boxes on the scene
        """
        return self.poly_items

    def rect_to_polygon(self, rect:QRect):
        return QPolygonF(rect.topLeft(),
                         rect.topRight(),
                         rect.bottomRight(),
                         rect.bottomLeft(),
                         rect.topLeft())  # to close the loop

class GraphicsViewWithMouse (QGraphicsView):
    mouse_moved_signal = pyqtSignal(float, float, name='mouse_moved')
    box_added_signal = pyqtSignal(QPolygonF, name='box_added')

    def __init__(self, scene = None):
        super(QGraphicsView, self).__init__(scene)
        self.scene = scene
        self.fixed_boxes_mode = False
        self.rubberBand = None

    def enable_fixed_boxes_mode(self, enable):
        self.fixed_boxes_mode = enable
        if not self.fixed_boxes_mode:
            self.clear_rubber_band()

    def clear_rubber_band(self):
        self.rubberBand.deleteLater()
        self.rubberBand = None

    def mousePressEvent(self, event):
        if not self.fixed_boxes_mode:
            return

        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.RubberBandDrag)

            self.origin = event.pos()
            if not self.rubberBand:
                self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()

    def mouseReleaseEvent(self, event):
        if not self.fixed_boxes_mode:
            return

        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)

            if self.rubberBand:
                selected_area = QRect(self.origin, event.pos())
                selected_area = self.mapToScene(selected_area)
                self.box_added_signal.emit(selected_area)

                self.clear_rubber_band()

    def mouseMoveEvent(self, event):
        relative_pos = self.mapToScene(event.pos())
        self.mouse_moved_signal.emit( relative_pos.x(), relative_pos.y())
        super().mouseMoveEvent(event)

        # update rubber band if mouse is dragging
        if self.dragMode():
            if self.rubberBand:
                self.rubberBand.setGeometry(QRect(self.origin, event.pos()))
