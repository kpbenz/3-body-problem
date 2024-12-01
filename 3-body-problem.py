#!/usr/bin/python3
"""Simulate the 3-Body-Problem in an artificial universe."""

import sys

from NBodyProblem.NBodyProblem import NBodyProblem

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QDoubleSpinBox

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore

# Planar simplification of the Sun-Earth-Moon System
# (only x and y coordinates)
#
# nbp = NBodyProblem()
# nbp.add_body("Sun",   True, 1.989e30,    0.0,         0.0,   0.0,  0.0,     0.0,  0.0)
# nbp.add_body("Earth", True, 5.972e24,  149.598023e9,  0.0,   0.0,  0.0, 29782.7,  0.0)
# nbp.add_body("Moon",  True, 7.348e22,  149.982630e9,  0.0,   0.0,  0.0, 30804.7,  0.0)

# Artificial Universe
nbp = NBodyProblem(g=0.0001, trail=2000)
nbp.add_body("Sun",   True, 1000.0,    0.0,  0.0,   0.0,  0.0,     0.0000,  0.0)
nbp.add_body("Earth", True,    2.0,    8.0,  0.0,   0.0,  0.0,     0.1110,  0.0)
nbp.add_body("Moon",  True,    0.8,    8.5,  0.0,   0.0,  0.0,     0.1044,  0.0400)


size = [0.5, 0.3, 0.1]
color = [(0.78, 0.55, 0.00, 1.0), (1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0)]

sp1 = gl.GLScatterPlotItem(pos=nbp.pos[0], size=size[0], color=color[0], pxMode=False)
sp1_trail = gl.GLScatterPlotItem(pos=nbp.pos[0], size=size[0]/5, color=color[0], pxMode=False)

sp2 = gl.GLScatterPlotItem(pos=nbp.pos[1], size=size[1], color=color[1], pxMode=False)
sp2_trail = gl.GLScatterPlotItem(pos=nbp.pos[1], size=size[1]/5, color=color[1], pxMode=False)

sp3 = gl.GLScatterPlotItem(pos=nbp.pos[2], size=size[2], color=color[2], pxMode=False)
sp3_trail = gl.GLScatterPlotItem(pos=nbp.pos[2], size=size[2]/5, color=color[2], pxMode=False)


def update():
    """Update plot data."""
    global sp1, sp2, sp3, nbp

    nbp.iterate()

    sp1.setData(pos=nbp.pos[0][-1])
    sp1_trail.setData(pos=nbp.pos[0])
    sp2.setData(pos=nbp.pos[1][-1])
    sp2_trail.setData(pos=nbp.pos[1])
    sp3.setData(pos=nbp.pos[2][-1])
    sp3_trail.setData(pos=nbp.pos[2])


class PlotWindow(QMainWindow):
    """Dynamic Plot window for 3-Body-Problem."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle('3-Body-Problem')
        self.resize(1600,1200)

        self.plot_graph = gl.GLViewWidget()

        self.setCentralWidget(self.plot_graph)

        self.plot_graph.setCameraPosition(distance=20)

        g = gl.GLGridItem()
        g.setSize(x=100, y=100, z=100)
        self.plot_graph.addItem(g)

        self.plot_graph.addItem(sp1)
        self.plot_graph.addItem(sp1_trail)

        self.plot_graph.addItem(sp2)
        self.plot_graph.addItem(sp2_trail)

        self.plot_graph.addItem(sp3)
        self.plot_graph.addItem(sp3_trail)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(25)
        self.timer.timeout.connect(update)


class MainWindow(QMainWindow):
    """Main window for 3-Body-Problem."""

    def __init__(self):
        super().__init__()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout()
        self.button_start = QPushButton("Start")
        self.button_start.setCheckable(True)
        self.button_start.clicked.connect(self.plot_start_button)
        # self.setCentralWidget(self.button)
        self.main_layout.addWidget(self.button_start)

        self.button_quit = QPushButton("Quit")
        self.button_quit.clicked.connect(self.quit_button)
        self.main_layout.addWidget(self.button_quit)

        self.spin_mass_1 = QDoubleSpinBox()
        self.spin_mass_1.setMinimum(0.0)
        self.spin_mass_1.setMaximum(100000.0)
        self.spin_mass_1.setSingleStep(100.0)
        self.spin_mass_1.valueChanged.connect(self.mass_changed_1)
        self.main_layout.addWidget(self.spin_mass_1)

        self.spin_mass_2 = QDoubleSpinBox()
        self.spin_mass_2.setMinimum(0.0)
        self.spin_mass_2.setMaximum(100000.0)
        self.spin_mass_2.setSingleStep(100.0)
        self.spin_mass_2.valueChanged.connect(self.mass_changed_2)
        self.main_layout.addWidget(self.spin_mass_2)

        self.spin_mass_3 = QDoubleSpinBox()
        self.spin_mass_3.setMinimum(0.0)
        self.spin_mass_3.setMaximum(100000.0)
        self.spin_mass_3.setSingleStep(100.0)
        self.spin_mass_3.valueChanged.connect(self.mass_changed_3)
        self.main_layout.addWidget(self.spin_mass_3)


        self.main_widget.setLayout(self.main_layout)

        self.plot_window = PlotWindow()
        self.plot_window.show()

    def plot_start_button(self, checked):
        """Open plot window."""
        if checked:
            self.plot_window.timer.start()
            self.button_start.setText("Stop")
        else:
            self.plot_window.timer.stop()
            self.button_start.setText("Start")

    def quit_button(self, checked):
        """Quit application."""
        sys.exit(0)

    def mass_changed_1(self, mass):
        nbp.set_body_mass(nbp.get_body_name(0),mass)


    def mass_changed_2(self, mass):
        nbp.set_body_mass(nbp.get_body_name(1),mass)


    def mass_changed_3(self, mass):
        nbp.set_body_mass(nbp.get_body_name(2),mass)




if __name__ == '__main__':

    app = QApplication([])
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
