
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtWidgets import (QApplication, QGraphicsEllipseItem,
                             QGraphicsScene, QGraphicsView, QWidget)

from cave_generation import *
from eller_algo import *
from shortest_path import *


class MovingDots(QGraphicsEllipseItem):
    """
        Класс для отрисовки начальной и конечной точки в решении лабиринта с функциями для их перемещения с помощью мыши

    """
    def __init__(self, x, y, r):
        super().__init__(0,0,r,r)
        self.setPos(x, y)
        self.setBrush(Qt.white)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        app.setOverrideCursor(Qt.OpenHandCursor)
        
    def hoverLeaveEvent(self, event):
        app.restoreOverrideCursor()

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))


class Ui_Lamborghini(object):
    """
        Класс для создания графического пользовательского интерфейса

    """

    def __init__(self):
        self.__scene = QGraphicsScene()
        self.__matrix_right_lines = np.array([0])
        self.__matrix_bottom_lines = np.array([0])
        self.__cave_matrix = np.array([0])

    def setupUi(self, Lamborghini):
        Lamborghini.setObjectName("Lamborghini")
        Lamborghini.setEnabled(True)
        Lamborghini.resize(821, 768)
        Lamborghini.setMinimumSize(QtCore.QSize(821, 768))
        Lamborghini.setMaximumSize(QtCore.QSize(821, 768))
        Lamborghini.setMouseTracking(True)
        self.width = QtWidgets.QSpinBox(Lamborghini)
        self.width.setGeometry(QtCore.QRect(680, 90, 81, 51))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.width.setFont(font)
        self.width.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.width.setAutoFillBackground(False)
        self.width.setStyleSheet("    border-radius: 20px;")
        self.width.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.width.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.width.setMinimum(2)
        self.width.setMaximum(50)
        self.width.setObjectName("width")
        self.height = QtWidgets.QSpinBox(Lamborghini)
        self.height.setGeometry(QtCore.QRect(550, 90, 81, 51))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.height.setFont(font)
        self.height.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.height.setAutoFillBackground(False)
        self.height.setStyleSheet("    border-radius: 20px;")
        self.height.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.height.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.height.setMinimum(2)
        self.height.setMaximum(50)
        self.height.setObjectName("height")
        self.download = QtWidgets.QPushButton(Lamborghini)
        self.download.setEnabled(True)
        self.download.setGeometry(QtCore.QRect(528, 166, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.download.setFont(font)
        self.download.setFocusPolicy(QtCore.Qt.NoFocus)
        self.download.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.download.setAutoFillBackground(False)
        self.download.setStyleSheet("QPushButton\n"
"{\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(176, 90, 35);\n"
"    border-radius: 20px;\n"
"    border: none;\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(177, 111, 55)\n"
"}\n"
"")
        self.download.setCheckable(False)
        self.download.setAutoDefault(False)
        self.download.setObjectName("download")
        self.generate = QtWidgets.QPushButton(Lamborghini)
        self.generate.setEnabled(True)
        self.generate.setGeometry(QtCore.QRect(528, 238, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.generate.setFont(font)
        self.generate.setStyleSheet("QPushButton\n"
"{\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(176, 90, 35);\n"
"    border-radius: 20px;\n"
"    border: none;\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(177, 111, 55)\n"
"}")
        self.generate.setObjectName("generate")
        self.label = QtWidgets.QLabel(Lamborghini)
        self.label.setGeometry(QtCore.QRect(528, 41, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Lamborghini)
        self.label_2.setGeometry(QtCore.QRect(540, 3, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setStyleSheet("color: rgb(255, 105, 48)")
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.graphicsView = QtWidgets.QGraphicsView(Lamborghini)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 502, 502))
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setLineWidth(2)
        self.graphicsView.setSceneRect(QtCore.QRectF(0.0, 0.0, 500.0, 500.0))
        self.graphicsView.setObjectName("graphicsView")
        self.road = QtWidgets.QPushButton(Lamborghini)
        self.road.setEnabled(True)
        self.road.setGeometry(QtCore.QRect(530, 380, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.road.setFont(font)
        self.road.setFocusPolicy(QtCore.Qt.NoFocus)
        self.road.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.road.setAutoFillBackground(False)
        self.road.setStyleSheet("QPushButton\n"
"{\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(176, 90, 35);\n"
"    border-radius: 20px;\n"
"    border: none;\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(177, 111, 55)\n"
"}\n"
"")
        self.road.setCheckable(False)
        self.road.setAutoDefault(False)
        self.road.setObjectName("road")
        self.label_3 = QtWidgets.QLabel(Lamborghini)
        self.label_3.setGeometry(QtCore.QRect(20, 518, 261, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setStyleSheet("color: rgb(255, 105, 48)")
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.cave_download = QtWidgets.QPushButton(Lamborghini)
        self.cave_download.setEnabled(True)
        self.cave_download.setGeometry(QtCore.QRect(310, 560, 230, 75))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.cave_download.setFont(font)
        self.cave_download.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cave_download.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.cave_download.setAutoFillBackground(False)
        self.cave_download.setStyleSheet("QPushButton\n"
"{\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(176, 90, 35);\n"
"    border-radius: 20px;\n"
"    border: none;\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(177, 111, 55)\n"
"}\n"
"")
        self.cave_download.setCheckable(False)
        self.cave_download.setAutoDefault(False)
        self.cave_download.setObjectName("cave_download")
        self.label_4 = QtWidgets.QLabel(Lamborghini)
        self.label_4.setGeometry(QtCore.QRect(10, 650, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.deth_limit = QtWidgets.QSpinBox(Lamborghini)
        self.deth_limit.setGeometry(QtCore.QRect(180, 607, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.deth_limit.setFont(font)
        self.deth_limit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.deth_limit.setAutoFillBackground(False)
        self.deth_limit.setStyleSheet("    border-radius: 20px;")
        self.deth_limit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.deth_limit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.deth_limit.setMaximum(7)
        self.deth_limit.setObjectName("deth_limit")
        self.birth_limit = QtWidgets.QSpinBox(Lamborghini)
        self.birth_limit.setGeometry(QtCore.QRect(51, 607, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.birth_limit.setFont(font)
        self.birth_limit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.birth_limit.setAutoFillBackground(False)
        self.birth_limit.setStyleSheet("    border-radius: 20px;")
        self.birth_limit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.birth_limit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.birth_limit.setMaximum(7)
        self.birth_limit.setObjectName("birth_limit")
        self.cftsi = QtWidgets.QSpinBox(Lamborghini)
        self.cftsi.setGeometry(QtCore.QRect(200, 700, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.cftsi.setFont(font)
        self.cftsi.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cftsi.setAutoFillBackground(False)
        self.cftsi.setStyleSheet("    border-radius: 20px;")
        self.cftsi.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cftsi.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.cftsi.setMinimum(1)
        self.cftsi.setMaximum(100)
        self.cftsi.setObjectName("cftsi")
        self.cave_generate = QtWidgets.QPushButton(Lamborghini)
        self.cave_generate.setEnabled(True)
        self.cave_generate.setGeometry(QtCore.QRect(310, 660, 230, 75))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.cave_generate.setFont(font)
        self.cave_generate.setStyleSheet("QPushButton\n"
"{\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(176, 90, 35);\n"
"    border-radius: 20px;\n"
"    border: none;\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(177, 111, 55)\n"
"}")
        self.cave_generate.setObjectName("cave_generate")
        self.manual_step = QtWidgets.QPushButton(Lamborghini)
        self.manual_step.setEnabled(True)
        self.manual_step.setGeometry(QtCore.QRect(560, 560, 230, 75))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.manual_step.setFont(font)
        self.manual_step.setStyleSheet("QPushButton\n"
"{\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(176, 90, 35);\n"
"    border-radius: 20px;\n"
"    border: none;\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(177, 111, 55)\n"
"}")
        self.manual_step.setObjectName("manual_step")
        self.auto_step = QtWidgets.QPushButton(Lamborghini)
        self.auto_step.setEnabled(True)
        self.auto_step.setGeometry(QtCore.QRect(560, 660, 160, 75))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.auto_step.setFont(font)
        self.auto_step.setStyleSheet("QPushButton\n"
"{\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(176, 90, 35);\n"
"    border-radius: 20px;\n"
"    border: none;\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(177, 111, 55)\n"
"}")
        self.auto_step.setObjectName("auto_step")
        self.step_speed = QtWidgets.QSpinBox(Lamborghini)
        self.step_speed.setGeometry(QtCore.QRect(733, 670, 71, 51))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.step_speed.setFont(font)
        self.step_speed.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.step_speed.setAutoFillBackground(False)
        self.step_speed.setStyleSheet("    border-radius: 20px;")
        self.step_speed.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.step_speed.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.step_speed.setMinimum(1)
        self.step_speed.setMaximum(1000)
        self.step_speed.setObjectName("step_speed")
        self.label_5 = QtWidgets.QLabel(Lamborghini)
        self.label_5.setGeometry(QtCore.QRect(750, 720, 51, 16))
        self.label_5.setObjectName("label_5")
        self.print_road = QtWidgets.QPushButton(Lamborghini)
        self.print_road.setEnabled(True)
        self.print_road.setGeometry(QtCore.QRect(530, 450, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.print_road.setFont(font)
        self.print_road.setFocusPolicy(QtCore.Qt.NoFocus)
        self.print_road.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.print_road.setAutoFillBackground(False)
        self.print_road.setStyleSheet("QPushButton\n"
"{\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(176, 90, 35);\n"
"    border-radius: 20px;\n"
"    border: none;\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(177, 111, 55)\n"
"}\n"
"")
        self.print_road.setCheckable(False)
        self.print_road.setAutoDefault(False)
        self.print_road.setObjectName("print_road")
        self.label_6 = QtWidgets.QLabel(Lamborghini)
        self.label_6.setGeometry(QtCore.QRect(10, 560, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.height_cave = QtWidgets.QSpinBox(Lamborghini)
        self.height_cave.setGeometry(QtCore.QRect(20, 700, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.height_cave.setFont(font)
        self.height_cave.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.height_cave.setAutoFillBackground(False)
        self.height_cave.setStyleSheet("    border-radius: 20px;")
        self.height_cave.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.height_cave.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.height_cave.setMinimum(2)
        self.height_cave.setMaximum(50)
        self.height_cave.setObjectName("height_cave")
        self.width_cave = QtWidgets.QSpinBox(Lamborghini)
        self.width_cave.setGeometry(QtCore.QRect(110, 700, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.width_cave.setFont(font)
        self.width_cave.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.width_cave.setAutoFillBackground(False)
        self.width_cave.setStyleSheet("    border-radius: 20px;")
        self.width_cave.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.width_cave.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.width_cave.setMinimum(2)
        self.width_cave.setMaximum(50)
        self.width_cave.setObjectName("width_cave")
        self.save_maze = QtWidgets.QPushButton(Lamborghini)
        self.save_maze.setEnabled(True)
        self.save_maze.setGeometry(QtCore.QRect(530, 307, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.save_maze.setFont(font)
        self.save_maze.setStyleSheet("QPushButton\n"
"{\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: rgb(176, 90, 35);\n"
"    border-radius: 20px;\n"
"    border: none;\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(177, 111, 55)\n"
"}")
        self.save_maze.setObjectName("save_maze")
        self.label_2.setBuddy(Lamborghini)
        self.label_3.setBuddy(Lamborghini)

        self.retranslateUi(Lamborghini)
        QtCore.QMetaObject.connectSlotsByName(Lamborghini)

        self.on_download_clicked()
        self.on_find_road_clicked()
        self.on_generate_clicked()
        self.on_download_cave_click()
        self.on_manual_step_click()
        self.on_generate_cave_click()
        self.on_auto_step_click()
        self.on_find_path_click()
        self.on_save_maze_click()

    def retranslateUi(self, Lamborghini):
        _translate = QtCore.QCoreApplication.translate
        Lamborghini.setWindowTitle(_translate("Lamborghini", "Widget"))
        self.download.setText(_translate("Lamborghini", "Download"))
        self.generate.setText(_translate("Lamborghini", "Generate"))
        self.label.setText(_translate("Lamborghini", "             height                        width "))
        self.label_2.setText(_translate("Lamborghini", "Choose maze size:"))
        self.road.setText(_translate("Lamborghini", "Start / End Positions"))
        self.label_3.setText(_translate("Lamborghini", "Choose cave parameters:"))
        self.cave_download.setText(_translate("Lamborghini", "Download"))
        self.label_4.setText(_translate("Lamborghini", "       height           width        alive probality"))
        self.cave_generate.setText(_translate("Lamborghini", "Generate"))
        self.manual_step.setText(_translate("Lamborghini", "Manual step"))
        self.auto_step.setText(_translate("Lamborghini", "Auto steps"))
        self.label_5.setText(_translate("Lamborghini", "speed"))
        self.print_road.setText(_translate("Lamborghini", "Find Road"))
        self.label_6.setText(_translate("Lamborghini", "      \"birth\" limit                \"death\" limit"))
        self.save_maze.setText(_translate("Lamborghini", "Save Maze"))

    def on_download_cave_click(self):
        self.cave_download.clicked.connect(lambda: self.open_file_cave())

    def on_download_clicked(self):
        self.download.clicked.connect(lambda: self.open_file_maze())

    def on_generate_clicked(self):
        self.generate.clicked.connect(lambda: self.mase_generate())

    def on_manual_step_click(self):
        self.manual_step.clicked.connect(lambda :self.cave_step())
    def on_generate_cave_click(self):
        self.cave_generate.clicked.connect(lambda :self.cave_generatuion())
    def on_auto_step_click(self):
        self.auto_step.clicked.connect(lambda :self.cave_auto_step())
    def on_find_path_click(self):
        self.road.clicked.connect(lambda: self.draw_two_dots())
    def on_find_road_clicked(self):
        self.print_road.clicked.connect(lambda: self.find_road())
    def on_save_maze_click(self):
        self.save_maze.clicked.connect(lambda: self.saving_maze())

    def draw_lines(self, matrix1, matrix2):
        scene = QGraphicsScene()
        self.graphicsView.setScene(scene)
        orange_color = QColor(176, 90, 35)
        pen = QPen(orange_color, 2, Qt.SolidLine)
        scene.addLine(0, 0, 500, 0, pen)
        scene.addLine(0, 0, 0, 500, pen)
        h, w = matrix1.shape
        tile_w = 500 / w
        tile_h = 500 / h
        for i in range(h):
            for j in range(w):
                if matrix1[i, j] == 1:
                    scene.addLine(j * tile_w + tile_w, i * tile_h, j * tile_w + tile_w, i * tile_h + tile_h, pen)
                if matrix2[i, j] == 1:
                    scene.addLine(j * tile_w, i * tile_h + tile_h, j * tile_w + tile_w, i * tile_h + tile_h, pen)
        self.__scene = scene

    def draw_rect(self, matrix1):
        scene = QGraphicsScene()
        self.graphicsView.setScene(scene)
        orange_color = QColor(176, 90, 35)
        pen = QPen(orange_color, 2, Qt.SolidLine)
        brush = QBrush(orange_color)
        h, w = matrix1.shape
        tile_w = 500 / w
        tile_h = 500 / h
        for i in range(h):
            for j in range(w):
                if matrix1[i, j] == 1:
                    scene.addRect(j * tile_w, i * tile_h, tile_w, tile_h, pen, brush)
        self.__cave_matrix = matrix1
        self.__scene = scene
        self.height_cave.setValue(h)
        self.width_cave.setValue(w)

    def open_file(self):
        try:
            self.width.setValue(0)
            self.height.setValue(0)
            file_path = QtWidgets.QFileDialog.getOpenFileName(Lamborghini, "Choose OBJ file", "/Users/", "TXT Files (*.txt)")[0]
            with open(file_path, "r") as file_text:
                m = file_text.readlines()
                h, w = m[0].split()
                m.pop(0)
                l_matrix = [list(map(int, i.split())) for i in m]
            return w, h, l_matrix
        except Exception:
            pass

    def open_file_maze(self):
        try:
            w, h, l_matrix = self.open_file()
            self.width.setValue(int(w))
            self.height.setValue(int(h))
            matrix1 = [l_matrix[i] for i in range(int(h))]
            matrix2 = [l_matrix[i] for i in range(len(matrix1) + 1, len(l_matrix))]
            matrix_right_lines = np.array(matrix1)
            matrix_bottom_lines = np.array(matrix2)
            self.__matrix_right_lines = matrix_right_lines
            self.__matrix_bottom_lines = matrix_bottom_lines
            self.draw_lines(matrix_right_lines, matrix_bottom_lines)
        except Exception:
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet(
                """
                QMessageBox {
                font: italic bold 18px;
                border-radius: 20px;
                }
                """
            )
            msg.setText("Try another FILE!")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.exec_()

    def open_file_cave(self):
        try:
            w, h, l_matrix = self.open_file()
            matrix1 = [l_matrix[i] for i in range(int(h))]
            matrix_lines = np.array(matrix1)
            self.draw_rect(matrix_lines)
        except Exception:
            pass

    def mase_generate(self):
        if self.height.value() < 2 or self.width.value() < 2:
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet(
                """
                QMessageBox {
                font: italic bold 18px;
                border-radius: 20px;
                }
                """
            )
            msg.setText("The size of the maze should be greater than 1 x 1!")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.exec_()
        else:
            matrix1, matrix2 = generate_maze(self.height.value(), self.width.value())
            self.__matrix_right_lines = matrix1
            self.__matrix_bottom_lines = matrix2
            self.draw_lines(matrix1, matrix2)

    def cave_step(self):
        if self.__cave_matrix.shape[0] < 2:
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet(
                """
                QMessageBox {
                font: italic bold 18px;
                border-radius: 20px;
                }
                """
            )
            msg.setText("Download or Generate Cave!")
            msg.exec_()
        else:
            matrix1 = self.__cave_matrix
            birth = self.birth_limit.value()
            death = self.deth_limit.value()
            new_matrix = cave_step_1(matrix1, birth, death)
            if not np.array_equal(matrix1, new_matrix):
                self.draw_rect(new_matrix)
                return True
            else:
                msg = QtWidgets.QMessageBox()
                msg.setStyleSheet(
                    """
                    QMessageBox {
                    font: italic bold 18px;
                    border-radius: 20px;
                    }
                    """
                )
                msg.setText("FINISH")
                msg.exec_()
                return False

    def cave_generatuion(self):
        rows, cols = self.height_cave.value(), self.width_cave.value()
        ap = self.cftsi.value()
        cave = cave_generatuion_1(rows, cols, ap)
        self.draw_rect(cave)

    def cave_auto_step(self):
        speed = self.step_speed.value() / 60
        flag = True
        while flag:
            flag = self.cave_step()
            QtWidgets.QApplication.processEvents()
            time.sleep(speed)

    def draw_two_dots(self):
        if self.__scene.width() == 0:
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet(
                """
                QMessageBox {
                font: italic bold 18px;
                border-radius: 20px;
                }
                """
            )
            msg.setText("Download or Generate maze!")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.exec_()
        else:
            self.draw_lines(self.__matrix_right_lines, self.__matrix_bottom_lines)
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet(
                """
                QMessageBox {
                font: italic bold 18px;
                border-radius: 20px;
                }
                """
            )
            msg.setText("Move points to find the road")
            msg.exec_()
            self.moveObject1 = MovingDots(2,2,7)
            self.moveObject2 = MovingDots(490, 490, 7)
            self.__scene.addItem(self.moveObject1)
            self.__scene.addItem(self.moveObject2)

    def find_road(self):
        if self.__scene.width() == 0:
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet(
                """
                QMessageBox {
                font: italic bold 18px;
                border-radius: 20px;
                }
                """
            )
            msg.setText("Download or Generate maze!")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.exec_()
        else:
            start, end = (self.moveObject1.pos().x(), self.moveObject1.pos().y()), (self.moveObject2.pos().x(), self.moveObject2.pos().y())
            start_idx = (int(start[1] / (500 /self.height.value())), int(start[0] / (500 / self.width.value())))
            end_idx = (int(end[1] / (500 /self.height.value())), int(end[0] / (500 / self.width.value())))
            path = find_shortest_path(self.__matrix_right_lines, self.__matrix_bottom_lines, start_idx, end_idx)
            self.print_path(path, self.__scene)

    def print_path(self, path: list, scene):
        color = QColor(250, 250, 250)
        pen = QPen(color, 2, Qt.SolidLine)
        for i in range(1, len(path)):
            y1, x1 = path[i]
            y, x = path[i - 1]
            h, w = self.__matrix_bottom_lines.shape
            x1, x = int((500 / w) * x1 + (500 / w) / 2), int((500 / w) * x + (500 / w) / 2)
            y1, y = int((500 / h) * y1 + (500 / h) / 2), int((500 / h) * y + (500 / h) / 2)
            scene.addLine(x, y, x1, y1, pen)

    def saving_maze(self):
        if self.__scene.width() == 0:
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet(
                """
                QMessageBox {
                font: italic bold 18px;
                border-radius: 20px;
                }
                """
            )
            msg.setText("Download or Generate maze!")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.exec_()
        else:
            try:
                file_path = \
                QtWidgets.QFileDialog.getSaveFileName(Lamborghini, "Select Output file", "/Users/", "TXT Files (*.txt)")[0]
                with open(file_path, "w") as f:
                    l = self.__matrix_bottom_lines.shape
                    f.write(' '.join(map(str, l)))
                    f.write('\n')
                    f.write('\n'.join([' '.join(map(str, line)) for line in self.__matrix_right_lines]))
                    f.write('\n')
                    f.write('\n')
                    f.write('\n'.join([' '.join(map(str, line)) for line in self.__matrix_bottom_lines]))
            except Exception:
                msg = QtWidgets.QMessageBox()
                msg.setStyleSheet(
                    """
                    QMessageBox {
                    font: italic bold 18px;
                    border-radius: 20px;
                    }
                    """
                )
                msg.setText("Try again")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Lamborghini = QtWidgets.QWidget()
    ui = Ui_Lamborghini()
    ui.setupUi(Lamborghini)
    Lamborghini.show()
    sys.exit(app.exec_())
