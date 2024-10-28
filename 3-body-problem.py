#!/usr/bin/python3
"""Demonstrates use of GLScatterPlotItem with rapidly-updating plots."""

from NBodyProblem.NBodyProblem import NBodyProblem


import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore

app = pg.mkQApp("3-Body-Problem")
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('3-Body-Problem')
w.setCameraPosition(distance=20)

g = gl.GLGridItem()
g.setSize(x=100,y=100,z=100)
w.addItem(g)


# Planar simplification of the Sun-Earth-Moon System
# (only x and y coordinates)
#
# nbp = NBodyProblem()
# nbp.add_body("Sun",   True, 1.989e30,    0.0,         0.0,   0.0,  0.0,     0.0,  0.0)
# nbp.add_body("Earth", True, 5.972e24,  149.598023e9,  0.0,   0.0,  0.0, 29782.7,  0.0)
# nbp.add_body("Moon",  True, 7.348e22,  149.982630e9,  0.0,   0.0,  0.0, 30804.7,  0.0)

# Artificial Universe
nbp = NBodyProblem(g=0.0001,trail=2000)
nbp.add_body("Sun",   True, 1000.0,    0.0,  0.0,   0.0,  0.0,     0.0000,  0.0)
nbp.add_body("Earth", True,    2.0,    8.0,  0.0,   0.0,  0.0,     0.1118,  0.0)
nbp.add_body("Moon",  True,    0.8,    8.5,  0.0,   0.0,  0.0,     0.1044,  0.0400)


size = [0.5, 0.3, 0.1]
color = [(0.78, 0.55, 0.00, 1.0), (1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0)]

sp1 = gl.GLScatterPlotItem(pos=nbp.pos[0], size=size[0], color=color[0], pxMode=False)
w.addItem(sp1)
sp1_trail = gl.GLScatterPlotItem(pos=nbp.pos[0], size=size[0]/3, color=color[0], pxMode=False)
w.addItem(sp1_trail)

sp2 = gl.GLScatterPlotItem(pos=nbp.pos[1], size=size[1], color=color[1], pxMode=False)
w.addItem(sp2)
sp2_trail = gl.GLScatterPlotItem(pos=nbp.pos[1], size=size[1]/3, color=color[1], pxMode=False)
w.addItem(sp2_trail)

sp3 = gl.GLScatterPlotItem(pos=nbp.pos[2], size=size[2], color=color[2], pxMode=False)
w.addItem(sp3)
sp3_trail = gl.GLScatterPlotItem(pos=nbp.pos[2], size=size[2]/3, color=color[2], pxMode=False)
w.addItem(sp3_trail)


def update():
    """Update plot data."""
   # global sp1, sp2, sp3 nbp

    nbp.iterate()

    sp1.setData(pos=nbp.pos[0][-1])
    sp1_trail.setData(pos=nbp.pos[0])
    sp2.setData(pos=nbp.pos[1][-1])
    sp2_trail.setData(pos=nbp.pos[1])
    sp3.setData(pos=nbp.pos[2][-1])
    sp3_trail.setData(pos=nbp.pos[2])


t = QtCore.QTimer()
t.timeout.connect(update)
t.start(25)

if __name__ == '__main__':
    pg.exec()
