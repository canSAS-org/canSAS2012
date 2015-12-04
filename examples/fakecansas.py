#!/usr/bin/env python

import numpy as np
import sys
import inspect
import time

import hdffile
import xmlfile

FILE_TIMESTAMP = time.strftime("%Y-%m-%dT%H:%M:%S")
FILE_TIMESTAMP += '%+03d%02d' % (-time.timezone/60/60, abs(time.timezone/60) % 60)
FILE_PRODUCER = "canSAS"

class ExampleFile:
    def __init__(self, writer):
        self.writer = writer
        np.random.seed(0)
    def write(self):
        pass

class SimpleExampleFile(ExampleFile):
    def write(self):
        self.writer.createFile()
        self.writer.createEntry("sasentry01")
        self.writer.createData("sasdata01", np.array([0]), ["Q",])
        self.writer.createDataSet("Q", np.random.rand(100,), {"units": "1/A"})
        self.writer.createDataSet("I", np.random.rand(100,), {"units": "1/cm"})
        self.writer.closeFile()

class Simple1DTimeSeries(ExampleFile):
    def write(self):
        self.writer.createFile()
        self.writer.createEntry("sasentry01")
        self.writer.createData("sasdata01", np.array([1]), ["Time","Q"])
        self.writer.createDataSet("Q", np.random.rand(100,), {"units": "1/A"})
        self.writer.createDataSet("I", np.random.rand(10,100,), {"units": "1/cm"})
        self.writer.createDataSet("Time", np.random.rand(10,), {"units": "s"})
        self.writer.closeFile()

class Generic1DTimeSeries(ExampleFile):
    def write(self):
        self.writer.createFile()
        self.writer.createEntry("sasentry01")
        self.writer.createData("sasdata01", np.array([0,1]), ["Time","Q"])
        self.writer.createDataSet("Q", np.random.rand(10,100,), {"units": "1/A"})
        self.writer.createDataSet("I", np.random.rand(10,100,), {"units": "1/cm"})
        self.writer.createDataSet("Time", np.random.rand(10,), {"units": "s"})
        self.writer.closeFile()

class Simple2DCase(ExampleFile):
    def write(self):
        self.writer.createFile()
        self.writer.createEntry("sasentry01")
        self.writer.createData("sasdata01", np.array([0,1]), ["Q","Q"])
        self.writer.createDataSet("Qx", np.random.rand(256,100,), {"units": "1/A"})
        self.writer.createDataSet("Qy", np.random.rand(256,100,), {"units": "1/A"})
        self.writer.createDataSet("Qz", np.random.rand(256,100,)*0, {"units": "1/A"})
        self.writer.createDataSet("I", np.random.rand(256,100,), {"units": "1/cm"})
        self.writer.closeFile()


class Simple2DMaskedCase(ExampleFile):
    def write(self):
        self.writer.createFile()
        self.writer.createEntry("sasentry01")
        self.writer.createData("sasdata01", np.array([0,1]), ["Q","Q"], {"Mask_indices": np.array([0,1])})
        self.writer.createDataSet("Qx", np.random.rand(256,100,), {"units": "1/A"})
        self.writer.createDataSet("Qy", np.random.rand(256,100,), {"units": "1/A"})
        self.writer.createDataSet("Qz", np.random.rand(256,100,)*0, {"units": "1/A"})
        self.writer.createDataSet("I", np.random.rand(256,100,), {"units": "1/cm"})
        self.writer.createDataSet("Mask", np.array(np.random.randint(0,1,256*100,).reshape(256,100), dtype=np.dtype("int8")))
        self.writer.closeFile()


class Generic2DCase(ExampleFile):
    def write(self):
        self.writer.createFile()
        self.writer.createEntry("sasentry01")
        self.writer.createData("sasdata01", np.array([0]), ["Q"])
        self.writer.createDataSet("Qx", np.random.rand(256*100,), {"units": "1/A"})
        self.writer.createDataSet("Qy", np.random.rand(256*100,), {"units": "1/A"})
        self.writer.createDataSet("Qz", np.random.rand(256*100,), {"units": "1/A"})
        self.writer.createDataSet("I", np.random.rand(256*100,), {"units": "1/cm"})
        self.writer.closeFile()


class Generic2DTimeSeries(ExampleFile):
    def write(self):
        self.writer.createFile()
        self.writer.createEntry("sasentry01")
        self.writer.createData("sasdata01", np.array([1]), ["Time","Q"], {"Time_indices" : np.array([0])})
        self.writer.createDataSet("Qx", np.random.rand(32*16,), {"units": "1/A"})
        self.writer.createDataSet("Qy", np.random.rand(32*16,), {"units": "1/A"})
        self.writer.createDataSet("Qz", np.random.rand(32*16,), {"units": "1/A"})
        self.writer.createDataSet("I", np.random.rand(11,32*16,), {"units": "1/cm"})
        self.writer.createDataSet("Time", np.random.rand(11,), {"units": "ms"})
        self.writer.closeFile()


class Generic2DQTimeSeries(ExampleFile):
    def write(self):
        self.writer.createFile()
        self.writer.createEntry("sasentry01")
        self.writer.createTitle('example of generic 2D SAS data in a time series, I(Q(t),t)')
        self.writer.createData("sasdata01", np.array([0,1]), ["Time","Q"])
        nx, ny, nt = (7, 5, 4)
        self.writer.createDataSet("Qx", np.random.rand(nt,nx*ny,), {"units": "1/A"})
        self.writer.createDataSet("Qy", np.random.rand(nt,nx*ny,), {"units": "1/A"})
        self.writer.createDataSet("Qz", np.random.rand(nt,nx*ny,), {"units": "1/A"})
        self.writer.createDataSet("I", np.random.rand(nt,nx*ny,), {"units": "1/cm"})
        self.writer.createDataSet("Time", np.random.rand(nt,), {"units": "ms"})
        self.writer.closeFile()


class Generic2DTimeTPSeries(ExampleFile):
    def write(self):
        self.writer.createFile()
        self.writer.createEntry("sasentry01")
        self.writer.createData("sasdata01", np.array([1,3,4]), ["Temperature","Time","Pressure","Q","Q"], {"Time_indices" : np.array([1]), "Temperature_indices" : np.array([0]), "Pressure_indices" : np.array([2])})
        self.writer.createDataSet("Qx", np.random.rand(7,3,3), {"units": "1/A"})
        self.writer.createDataSet("Qy", np.random.rand(7,3,3), {"units": "1/A"})
        self.writer.createDataSet("Qz", np.random.rand(7,3,3), {"units": "1/A"})
        self.writer.createDataSet("I", np.random.rand(3,7,2,3,3), {"units": "1/cm"})
        self.writer.createDataSet("Time", np.random.rand(7,), {"units": "ms"})
        self.writer.createDataSet("Temperature", np.random.rand(3,), {"units": "T"})
        self.writer.createDataSet("Pressure", np.random.rand(2,), {"units": "MPa"})
        self.writer.closeFile()


if __name__ == "__main__":
    subclasses = []
    classType=ExampleFile
    callers_module = sys._getframe(0).f_globals['__name__']
    classes = inspect.getmembers(sys.modules[callers_module], inspect.isclass)
    for name, obj in classes:
        if (obj is not classType) and (classType in inspect.getmro(obj)):
            subclasses.append((obj, name))
    for file in subclasses:
        filename = file[1].lower()
        exclazz = file[0]
        print "writing", exclazz
        for writer in [xmlfile.xmlfile, hdffile.hdffile]:
            exclazz(writer(filename, producer=FILE_PRODUCER, file_time=FILE_TIMESTAMP)).write()
