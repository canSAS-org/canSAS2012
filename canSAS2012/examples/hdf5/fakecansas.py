import numpy as np
import h5py
import os
import sys
import inspect
import traceback

class ExampleFile:

	def __init__(self, name, **keywords):
		self.name = name
		self.keywords = keywords

	def createFile(self):
		self.f = h5py.File(self.name, "w")
		self.f.attrs['file_name'] = self.name
		self.f.attrs['file_time'] = "2009-09-09T09:09:09-0000"
		self.f.attrs['producer'] = "canSAS"
		#self.f.attrs['HDF5_Version'] = h5py.version.hdf5_version
		#self.f.attrs['h5py_version'] = h5py.version.version

	def closeFile(self):
		self.f.close()

	def createEntry(self, name):
		self.sasentry = self.f.create_group(name)
		self.sasentry.attrs["NX_class"] = "SASentry"
		self.sasentry.attrs["version"] = "1.0"
	
	def createData(self, name, qi, ii, mi=None, attributes=None):
		self.sasdata = self.sasentry.create_group(name)
		self.sasdata.attrs["NX_class"] = "SASdata"
		self.sasdata.attrs["Q_indices"] = qi
		self.sasdata.attrs["I_axes"] = ii
		if mi != None:
			self.sasdata.attrs["Mask_indices"] = mi
		if attributes != None:
			for key in attributes.keys():
				self.sasdata.attrs[key] = attributes[key]

	def createDataSet(self, name, array, attributes=None):
		ds = self.sasdata.create_dataset(name, array.shape, data=array)
		if attributes != None:
			for key in attributes.keys():
				ds.attrs[key] = attributes[key]

class SimpleExampleFile(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([0]), "Q")
		self.createDataSet("Q", np.random.rand(100,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(100,), {"units": "1/cm"})
		self.closeFile()

class Simple1DTimeSeries(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([1]), "Time,Q")
		self.createDataSet("Q", np.random.rand(100,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(10,100,), {"units": "1/cm"})
		self.createDataSet("Time", np.random.rand(10,), {"units": "s"})
		self.closeFile()

class Generic1DTimeSeries(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([0,1]), "Time,Q")
		self.createDataSet("Q", np.random.rand(10,100,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(10,100,), {"units": "1/cm"})
		self.createDataSet("Time", np.random.rand(10,), {"units": "s"})
		self.closeFile()

class Simple2DCase(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([0,1]), "Q,Q")
		self.createDataSet("Q", np.random.rand(256,100,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(256,100,), {"units": "1/cm"})
		self.closeFile()


class Simple2DMaskedCase(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([0,1]), "Q,Q", np.array([0,1]))
		self.createDataSet("Q", np.random.rand(256,100,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(256,100,), {"units": "1/cm"})
		self.createDataSet("Mask", np.array(np.random.randint(0,1,256*100,).reshape(256,100), dtype=np.dtype("int8")))
		self.closeFile()


class Generic2DCase(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([0]), "Q")
		self.createDataSet("Q", np.random.rand(256*100,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(256*100,), {"units": "1/cm"})
		self.closeFile()


class Generic2DTimeSeries(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([0,1]), "Time,Q", None, {"Time_indices" : np.array([0])})
		self.createDataSet("Q", np.random.rand(33,256*100,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(33,256*100,), {"units": "1/cm"})
		self.createDataSet("Time", np.random.rand(33,), {"units": "ms"})
		self.closeFile()


class Generic2DTimeTPSeries(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", np.array([1,3,4]), "Temperature,Time,Pressure,Q,Q", None, {"Time_indices" : np.array([1]), "Temperature_indices" : np.array([0]), "Pressure_indices" : np.array([2])})
		self.createDataSet("Q", np.random.rand(7,3,3), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(3,7,2,3,3), {"units": "1/cm"})
		self.createDataSet("Time", np.random.rand(3,), {"units": "ms"})
		self.createDataSet("Temperature", np.random.rand(7,), {"units": "ms"})
		self.createDataSet("Pressure", np.random.rand(2,), {"units": "ms"})
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
       filename = file[1]+".h5"
       filename = filename.lower()
       file[0](filename).write()
       os.system("h5dump -A %s > %s.dump" % (filename, filename))


