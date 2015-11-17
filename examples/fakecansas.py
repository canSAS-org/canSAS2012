#!/usr/bin/env python

import numpy as np
import os
import sys
import inspect
import traceback
import time

# this is embarrassing, there is more at the end
#from hdffile import ExampleFile
from xmlfile import ExampleFile

FILE_TIMESTAMP = time.strftime("%Y-%m-%dT%H:%M:%S")
FILE_TIMESTAMP += '%+03d%02d' % (-time.timezone/60/60, abs(time.timezone/60) % 60)
FILE_PRODUCER = "canSAS"

class SimpleExampleFile(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([0]), ["Q",])
		self.createDataSet("Q", np.random.rand(100,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(100,), {"units": "1/cm"})
		self.closeFile()

class Simple1DTimeSeries(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([1]), ["Time","Q"])
		self.createDataSet("Q", np.random.rand(100,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(10,100,), {"units": "1/cm"})
		self.createDataSet("Time", np.random.rand(10,), {"units": "s"})
		self.closeFile()

class Generic1DTimeSeries(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([0,1]), ["Time","Q"])
		self.createDataSet("Q", np.random.rand(10,100,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(10,100,), {"units": "1/cm"})
		self.createDataSet("Time", np.random.rand(10,), {"units": "s"})
		self.closeFile()

class Simple2DCase(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([0,1]), ["Q","Q"])
		self.createDataSet("Qx", np.random.rand(256,100,), {"units": "1/A"})
		self.createDataSet("Qy", np.random.rand(256,100,), {"units": "1/A"})
		self.createDataSet("Qz", np.random.rand(256,100,)*0, {"units": "1/A"})
		self.createDataSet("I", np.random.rand(256,100,), {"units": "1/cm"})
		self.closeFile()


class Simple2DMaskedCase(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([0,1]), ["Q","Q"], {"Mask_indices": np.array([0,1])})
		self.createDataSet("Qx", np.random.rand(256,100,), {"units": "1/A"})
		self.createDataSet("Qy", np.random.rand(256,100,), {"units": "1/A"})
		self.createDataSet("Qz", np.random.rand(256,100,)*0, {"units": "1/A"})
		self.createDataSet("I", np.random.rand(256,100,), {"units": "1/cm"})
		self.createDataSet("Mask", np.array(np.random.randint(0,1,256*100,).reshape(256,100), dtype=np.dtype("int8")))
		self.closeFile()


class Generic2DCase(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([0]), ["Q"])
		self.createDataSet("Qx", np.random.rand(256*100,), {"units": "1/A"})
		self.createDataSet("Qy", np.random.rand(256*100,), {"units": "1/A"})
		self.createDataSet("Qz", np.random.rand(256*100,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(256*100,), {"units": "1/cm"})
		self.closeFile()


class Generic2DTimeSeries(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([1]), ["Time","Q"], {"Time_indices" : np.array([0])})
		self.createDataSet("Qx", np.random.rand(32*16,), {"units": "1/A"})
		self.createDataSet("Qy", np.random.rand(32*16,), {"units": "1/A"})
		self.createDataSet("Qz", np.random.rand(32*16,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(11,32*16,), {"units": "1/cm"})
		self.createDataSet("Time", np.random.rand(11,), {"units": "ms"})
		self.closeFile()


class Generic2DQTimeSeries(ExampleFile):
    def write(self):
        self.createFile()
        self.createEntry("sasentry01")
        self.createTitle('example of generic 2D SAS data in a time series, I(Q(t),t)')
        self.createData("sasdata01", np.array([0,1]), ["Time","Q"])
        nx, ny, nt = (7, 5, 4)
        self.createDataSet("Qx", np.random.rand(nt,nx*ny,), {"units": "1/A"})
        self.createDataSet("Qy", np.random.rand(nt,nx*ny,), {"units": "1/A"})
        self.createDataSet("Qz", np.random.rand(nt,nx*ny,), {"units": "1/A"})
        self.createDataSet("I", np.random.rand(nt,nx*ny,), {"units": "1/cm"})
        self.createDataSet("Time", np.random.rand(nt,), {"units": "ms"})
        self.closeFile()


class Generic2DTimeTPSeries(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([1,3,4]), ["Temperature","Time","Pressure","Q","Q"], {"Time_indices" : np.array([1]), "Temperature_indices" : np.array([0]), "Pressure_indices" : np.array([2])})
		self.createDataSet("Qx", np.random.rand(7,3,3), {"units": "1/A"})
		self.createDataSet("Qy", np.random.rand(7,3,3), {"units": "1/A"})
		self.createDataSet("Qz", np.random.rand(7,3,3), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(3,7,2,3,3), {"units": "1/cm"})
		self.createDataSet("Time", np.random.rand(7,), {"units": "ms"})
		self.createDataSet("Temperature", np.random.rand(3,), {"units": "T"})
		self.createDataSet("Pressure", np.random.rand(2,), {"units": "MPa"})
		self.closeFile()


if __name__ == "__main__":
    subclasses = []
    classType=ExampleFile
    callers_module = sys._getframe(0).f_globals['__name__']
    classes = inspect.getmembers(sys.modules[callers_module], inspect.isclass)
    for name, obj in classes:
        if (obj is not classType) and (classType in inspect.getmro(obj)):
            subclasses.append((obj, name))
    for file in subclasses:
       filename = "xml/"+file[1]+".xml"
       filename = filename.lower()
       file[0](filename).write()
    #for file in subclasses:
    #  filename = "hdf5/"+file[1]+".h5"
    #  filename = filename.lower()
    #  file[0](filename).write()
    #  os.system("h5dump -A %s > %s.dump" % (filename, filename))


