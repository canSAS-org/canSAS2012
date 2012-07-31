import numpy as np
import h5py
import os
import sys
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
		self.nxentry = self.f.create_group(name)
		self.nxentry.attrs["NX_class"] = "SASentry"
		self.nxentry.attrs["version"] = "1.0"
	
	def createData(self, name, qi, ii, mi=None):
		self.nxdata = self.nxentry.create_group(name)
		self.nxdata.attrs["NX_class"] = "SASdata"
		self.nxdata.attrs["Q_indices"] = qi
		self.nxdata.attrs["I_indices"] = ii
		if mi != None:
			self.nxdata.attrs["Mask_indices"] = mi

	def createDataSet(self, name, array, attributes=None):
		ds = self.nxdata.create_dataset(name, array.shape, data=array)
		if attributes != None:
			for key in attributes.keys():
				ds.attrs[key] = attributes[key]
		#nxdet.create_dataset("region_of_interest", (4,), dtype=np.dtype("int16"), data=np.array([160,114,907,834]))

class SimpleExampleFile(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", "*", "Q")
		#data = np.genfromtxt("silver.txt", delimiter="	", dtype=np.dtype("int16"))
		self.createDataSet("Q", np.random.rand(100,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(100,), {"units": "1/cm"})
		self.closeFile()


class Simple1DTimeSeries(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createData("sasdata01", ",*", "Time,Q")
		#data = np.genfromtxt("silver.txt", delimiter="	", dtype=np.dtype("int16"))
		self.createDataSet("Q", np.random.rand(100,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(10,100,), {"units": "1/cm"})
		self.createDataSet("Time", np.random.rand(10,), {"units": "s"})
		self.closeFile()


if __name__ == "__main__":
    SimpleExampleFile("simple.h5").write()
    Simple1DTimeSeries("simple1DTimeSeries.h5").write()

