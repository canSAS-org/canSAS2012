#!/usr/bin/env python

import h5py
import os

class hdffile:
    def __init__(self, name, **keywords):
        self.name = os.path.join("hdf5", name + ".h5")
        self.keywords = keywords

    def createFile(self):
        self.f = h5py.File(self.name, "w")
        self.f.attrs['file_name'] = self.name
        self.f.attrs['HDF5_Version'] = h5py.version.hdf5_version
        self.f.attrs['h5py_version'] = h5py.version.version
        for keyw in ["file_time", "producer"]:
             if keyw in self.keywords:
                   self.f.attrs[keyw] = self.keywords[keyw]

    def closeFile(self):
          self.f.close()
          os.system("h5dump -A %s > %s.dump" % (self.name, self.name))

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
