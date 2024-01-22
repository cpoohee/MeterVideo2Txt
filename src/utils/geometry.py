from PyQt5.QtGui import QPolygonF
def get_centroid_poly(polygon:QPolygonF):
    """https://en.wikipedia.org/wiki/Centroid#Of_a_polygon"""
    N = polygon.size()
    # minimal sanity check
    if N < 3:
        raise ValueError('At least 3 vertices must be passed.')
    sum_A, sum_Cx, sum_Cy = 0, 0, 0
    last_iteration = N - 1
    # from 0 to N-1
    for i in range(N):
        if i != last_iteration:
            shoelace = polygon[i].x() * polygon[i + 1].y() - polygon[
                i + 1].x() * polygon[i].y()
            sum_A += shoelace
            sum_Cx += (polygon[i].x() + polygon[i + 1].x()) * shoelace
            sum_Cy += (polygon[i].y() + polygon[i + 1].y()) * shoelace
        else:
            # N-1 case (last iteration): substitute i+1 -> 0
            shoelace = polygon[i].x() * polygon[0].y() - polygon[0].x() * \
                       polygon[i].y()
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

def convert_QPolygons_to_array(polygon:QPolygonF):
    arr = []
    for i in range(0, polygon.size()):
        arr.append(polygon[i].x())
        arr.append(polygon[i].y())
    return arr