#!/usr/bin/env python

import numpy as np
import sys
import inspect


from lxml import etree


CANSAS_VERSION = '1.0'
FILE_TIMESTAMP = "2009-09-09T09:09:09-0000"
FILE_PRODUCER = "canSAS"


class ExampleFile():
	'''Support for XML files'''
	rootTag = "SASroot"
	root = None
	filename = None
	entry = None
	sasdata = None
	
	def __init__(self, filename):
		self.filename = filename

	def createFile(self):
		'''creates the in-memory data structure - actual file creation happens in closeFile()'''
		self.root = etree.Element(self.rootTag)
		self.root.attrib['file_name'] = self.filename
		self.root.attrib['file_time'] = FILE_TIMESTAMP
		self.root.attrib['producer'] = FILE_PRODUCER
		#self.root.attrib['Python_etree_version'] = etree.__version__

	def closeFile(self):
		'''write (or overwrite) the named XML file'''
		if self.root is not None and self.filename is not None:
			text = etree.tostring(self.root, pretty_print=True, encoding='utf-8')
			f = open(self.filename, 'w')
			f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
			#if xslt != None:
			#	f.write('<?xml-stylesheet type="text/xsl" href="%s"?>\n' % xslt)
			f.write( text )
			f.close()

	def createEntry(self, name):
		if self.root is None:
			raise "No parent SASroot node created yet!"
		self.entry = etree.SubElement(self.root, 'SASentry')
		self.entry.attrib['name'] = name
		self.entry.attrib['version'] = CANSAS_VERSION
		self.sasdata = None

	def createTitle(self, title):
		if self.root is None:
			raise "No parent SASentry node created yet!"
		node = etree.SubElement(self.entry, 'Title')
		node.text = title
	
	def createData(self, name, qi, ii, mi=None):
		if self.entry is None:
			raise "No parent SASentry node created yet!"
		self.sasdata = etree.SubElement(self.entry, 'SASdata')
		self.sasdata.attrib['name'] = name
		self.sasdata.attrib['I_axes'] = ii
		items = self._list_to_text_list(qi)
		self.sasdata.attrib['Q_indices'] = items
		if mi != None:
			items = self._list_to_text_list(mi)
			self.sasdata.attrib['Mask_indices'] = items

	def createDataSet(self, name, array, attributes=None):
		if self.sasdata is None:
			raise "No parent SASdata node created yet!"
		node = etree.SubElement(self.entry, name)
		text = self._list_to_text_list(array.shape, delimiter='')
		node.attrib['size'] = text.strip('(),')
		node.text = self._list_to_text_list(array, delimiter=' ')
		if attributes != None:
			for key, value in attributes.items():
				node.attrib[key] = value
		
	def _list_to_text_list(self, data, delimiter = ','):
		return delimiter.join( str(data).strip('[]').split() )


class SimpleExampleFile(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createTitle('example of simple 1D SAS data, I(Q)')
		self.createData("sasdata01", np.array([0]), "Q")
		n = 11
		self.createDataSet("Q", np.random.rand(n,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(n,), {"units": "1/cm"})
		self.closeFile()

class Simple1DTimeSeries(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createTitle('example of simple 1D SAS data in a time series, I(Q, t)')
		self.createData("sasdata01", np.array([1]), "Time,Q")
		n = 11
		nt = 7
		self.createDataSet("Q", np.random.rand(n,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(nt,n,), {"units": "1/cm"})
		self.createDataSet("Time", np.random.rand(nt,), {"units": "s"})
		self.closeFile()

class Generic1DTimeSeries(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createTitle('example of generic 1D SAS data in a time series, I(Q(t), t)')
		self.createData("sasdata01", np.array([0,1]), "Time,Q")
		n = 11
		nt = 7
		self.createDataSet("Q", np.random.rand(nt,n,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(nt,n,), {"units": "1/cm"})
		self.createDataSet("Time", np.random.rand(nt,), {"units": "s"})
		self.closeFile()

class Simple2DCase(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createTitle('example of simple 2D (image) SAS data, I(Q)')
		self.createData("sasdata01", np.array([0,1]), "Q,Q")
		nx = 11
		ny = 5
		self.createDataSet("Q", np.random.rand(nx,ny,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(nx,ny,), {"units": "1/cm"})
		self.closeFile()


class Simple2DMaskedCase(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createTitle('example of a simple masked 2D (image) SAS data, I(Q)')
		self.createData("sasdata01", np.array([0,1]), "Q,Q", np.array([0,1]))
		nx = 11
		ny = 5
		self.createDataSet("Q", np.random.rand(nx,ny,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(nx,ny,), {"units": "1/cm"})
		self.createDataSet("Mask", np.array(np.random.randint(0,1,nx*ny,).reshape(nx,ny), dtype=np.dtype("int8")))
		self.closeFile()


class Generic2DCase(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createTitle('example of generic 2D SAS data, I(Q)')
		self.createData("sasdata01", np.array([0]), "Q")
		nx = 11
		ny = 5
		self.createDataSet("Q", np.random.rand(nx*ny,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(nx*ny,), {"units": "1/cm"})
		self.closeFile()


class Generic2DTimeSeries(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createTitle('example of generic 2D SAS data in a time series, I(Q(t),t)')
		self.createData("sasdata01", np.array([0,1]), "Time,Q")
		nx = 11
		ny = 5
		nt = 7
		self.createDataSet("Q", np.random.rand(nt,nx*ny,), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(nt,nx*ny,), {"units": "1/cm"})
		self.createDataSet("Time", np.random.rand(nt,), {"units": "ms"})
		self.closeFile()


class Generic2DTimeTPSeries(ExampleFile):
	def write(self):
		self.createFile()
		self.createEntry("sasentry01")
		self.createTitle('example of generic 2D SAS data in a time, T, & P series, I(t,T,P,Q(t,T,P))')
		self.createData("sasdata01", np.array([1,3,4]), "Temperature,Time,Pressure,Q,Q")
		nqx = 3
		nqy = 4
		ntime = 7
		ntemperature = 3
		npressure = 2
		self.createDataSet("Q", np.random.rand(ntime,nqx,nqy), {"units": "1/A"})
		self.createDataSet("I", np.random.rand(ntemperature,ntime,npressure,nqx,nqy), {"units": "1/cm"})
		self.createDataSet("Time", np.random.rand(ntime,), {"units": "ms"})
		self.createDataSet("Temperature", np.random.rand(ntemperature,), {"units": "ms"})
		self.createDataSet("Pressure", np.random.rand(npressure,), {"units": "ms"})
		self.closeFile()


def main():
	subclasses = []
	classType=ExampleFile
	callers_module = sys._getframe(0).f_globals['__name__']
	classes = inspect.getmembers(sys.modules[callers_module], inspect.isclass)
	for name, obj in classes:
		if (obj is not classType) and (classType in inspect.getmro(obj)):
			subclasses.append((obj, name))
	for f in subclasses:
		filename = f[1]+".xml"
		filename = filename.lower()
		f[0](filename).write()


if __name__ == "__main__":
	main()
