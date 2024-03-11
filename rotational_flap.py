import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QPainter, QPen, QPixmap, QColor
from PyQt5.QtCore import Qt, QPointF

class RotationalFlapRepair(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Rotational Flap Repair')
        self.setGeometry(100, 100, 400, 400)

        self.diameter_label = QLabel("Enter wound diameter length (any unit, recommended values 1-10):")
        self.diameter_input = QLineEdit()
        self.repair_button = QPushButton("Repair")
        self.repair_button.clicked.connect(self.repairClicked)

        self.label_distance_x_first = QLabel()
        self.label_distance_y_first = QLabel()

        self.label_distance_x_second = QLabel()
        self.label_distance_y_second = QLabel()


        self.canvas = QLabel()
        self.canvas.setAlignment(Qt.AlignCenter)
        self.drawCanvas()

        layout = QVBoxLayout()
        layout.addWidget(self.diameter_label)
        layout.addWidget(self.diameter_input)
        layout.addWidget(self.repair_button)
        layout.addWidget(self.label_distance_x_first)
        layout.addWidget(self.label_distance_y_first)
        layout.addWidget(self.label_distance_x_second)
        layout.addWidget(self.label_distance_y_second)
        layout.addWidget(self.canvas)


        self.setLayout(layout)

    def drawCanvas(self):
        diameter = self.getDiameter()
        if diameter is not None:
            pixmap = self.generatePixmap(diameter)
            self.canvas.setPixmap(pixmap)

    def generatePixmap(self, diameter):
        pixmap = QPixmap(700, 500)
        pixmap.fill(QColor(255, 204, 153))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        #Adjust Diameter
        diameter *= 10

        # Draw circle
        radius = diameter / 2
        center = QPointF(75, 350)
        pen = QPen(Qt.red)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawEllipse(center, radius, radius)

        painter.end()
        return pixmap

    def getDiameter(self):
        try:
            diameter = float(self.diameter_input.text())
            return diameter
        except ValueError:
            return None

    def repairClicked(self):
        diameter = self.getDiameter()
        if diameter is not None:
            pixmap = self.generatePixmap(diameter)
            painter = QPainter(pixmap)
            pen = QPen(Qt.black, 1, Qt.DotLine)
            pen.setWidth(3)
            painter.setPen(pen)

            #Adjust diameter
            diameter *=10

            # Draw bottom dotted line for repair
            radius = diameter / 2
            center = QPointF(75, 350)
            x1 = 75 - radius
            y1 = 350 + radius
            x1_end = x1 + diameter * 3
            end_point = QPointF(x1_end, y1)
            painter.drawLine(QPointF(x1,y1), end_point)

            # Draw top dotted line for repair
            x2 = end_point.x() - 3 * diameter * math.cos(math.atan(2/5))
            y2 = end_point.y() - 3 * diameter * math.sin(math.atan(2/5))
            painter.drawLine(QPointF(x2,y2), end_point)

            # Calculate the radius of the new circle based on the length requirement
            new_circle_radius = 3 * diameter
            new_circle_center = end_point

            # Calculate the angle needed to cover the desired arc length
            arc_length = 7 * diameter
            arc_angle = (arc_length / (2 * math.pi * new_circle_radius)) * 360

             # Calculate the start angle of the arc
            start_angle = math.degrees(math.atan2(y1 - new_circle_center.y(), x1 - new_circle_center.x()))

            # Draw the arc clockwise
            pen = QPen(Qt.black)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawArc(new_circle_center.x() - new_circle_radius, new_circle_center.y() - new_circle_radius,
                        new_circle_radius * 2, new_circle_radius * 2, start_angle * 16, -arc_angle * 16)

            # Calculate the start angle of the second arc
            start_angle_second = start_angle - arc_angle

            # Calculate the length of the second arc
            arc_length_second = 3 * diameter
            arc_angle_second = (arc_length_second / (2 * math.pi * new_circle_radius)) * 360

            # Draw the second arc clockwise
            pen = QPen(Qt.black, 1, Qt.DotLine)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawArc(new_circle_center.x() - new_circle_radius, new_circle_center.y() - new_circle_radius,
                        new_circle_radius * 2, new_circle_radius * 2, (start_angle_second - arc_angle_second) * 16, arc_angle_second * 16)

            
            # Calculate the end angle of the first arc
            end_angle = start_angle - arc_angle

            # Calculate the other endpoint of the first arc
            end_point_first = QPointF(new_circle_center.x() + new_circle_radius * math.cos(math.radians(end_angle)),
                                  new_circle_center.y() + new_circle_radius * math.sin(math.radians(end_angle)))

            # Calculate the endpoint of the second arc
            end_angle_second = start_angle_second - arc_angle_second
            end_point_second = QPointF(new_circle_center.x() + new_circle_radius * math.cos(math.radians(end_angle_second)),
                                   new_circle_center.y() + new_circle_radius * math.sin(math.radians(end_angle_second)))


            painter.end()
            self.canvas.setPixmap(pixmap)

            # Calculate the x and y distance from the center of the new circle to the end point of the first arc
            distance_x = round((end_point_first.x() - new_circle_center.x()) / 10, 1)
            distance_y = round((end_point_first.y() - new_circle_center.y()) / 10, 1)

            distance_x_second = round((end_point_second.x() - new_circle_center.x()) / 10, 1)
            distance_y_second = round((end_point_second.y() - new_circle_center.y()) / 10, 1)



            # Assuming you have labels to display these distances in your GUI
            self.label_distance_x_first.setText(f"X Distance to 5 x diameter from pivot point: {distance_x}")
            self.label_distance_y_first.setText(f"Y Distance to 5 x diameter from pivot point: {distance_y}")

            self.label_distance_x_second.setText(f"X Distance to 8 x diameter from pivot point: {distance_x_second}")
            self.label_distance_y_second.setText(f"Y Distance to 8 x diameter from pivot point: {distance_y_second}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RotationalFlapRepair()
    ex.show()
    sys.exit(app.exec_())
