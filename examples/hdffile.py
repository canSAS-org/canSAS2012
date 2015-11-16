#!/usr/bin/env python

import numpy as np
import h5py
import os
import sys
import inspect
import traceback
import time


FILE_TIMESTAMP = time.strftime("%Y-%m-%dT%H:%M:%S")
FILE_TIMESTAMP += '%+03d%02d' % (-time.timezone/60/60, abs(time.timezone/60) % 60)
FILE_PRODUCER = "canSAS"

class ExampleFile:
	def __init__(self, name, **keywords):
		self.name = name
		self.keywords = keywords

	def createFile(self):
		self.f = h5py.File(self.name, "w")
		self.f.attrs['file_name'] = self.name
		self.f.attrs['file_time'] = FILE_TIMESTAMP
		self.f.attrs['producer'] = FILE_PRODUCER
		#self.f.attrs['HDF5_Version'] = h5py.version.hdf5_version
		#self.f.attrs['h5py_version'] = h5py.version.version

	def closeFile(self):
		self.f.close()

	def createEntry(self, name):
		self.sasentry = self.f.create_group(name)
		self.sasentry.attrs["NX_class"] = "SASentry"
		self.sasentry.attrs["version"] = "1.0"
	
	def createTitle(self, title):
		self.sasentry.create_dataset('Title', (), data=title)
	
	def createData(self, name, qi, ii, attributes=None):
		self.sasdata = self.sasentry.create_group(name)
		self.sasdata.attrs["NX_class"] = "SASdata"
		self.sasdata.attrs["Q_indices"] = qi
		self.sasdata.attrs["I_axes"] = ii
		if attributes != None:
			for key in attributes.keys():
				self.sasdata.attrs[key] = attributes[key]

	def createDataSet(self, name, array, attributes=None):
		ds = self.sasdata.create_dataset(name, array.shape, data=array)
		if attributes != None:
			for key in attributes.keys():
				ds.attrs[key] = attributes[key]

