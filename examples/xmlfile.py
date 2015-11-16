#!/usr/bin/env python

'''
Generate synthetic data to demonstrate canSAS (2012) data structure in XML

:see: http://www.smallangles.net/wgwiki/index.php/2012_Data_Discussion_Examples
'''

import inspect
import string
import time
import sys
import numpy as np
from lxml import etree


CANSAS_VERSION = '1.0'
FILE_TIMESTAMP = time.strftime("%Y-%m-%dT%H:%M:%S")
FILE_TIMESTAMP += '%+03d%02d' % (-time.timezone/60/60, abs(time.timezone/60) % 60)
FILE_PRODUCER = "canSAS"


class ExampleFile():
    '''Support for creating and writing XML files (not reading)'''
    rootTag = "SASroot"
    root = None
    filename = None
    entry = None
    sasdata = None
    
    def __init__(self, filename):
        self.filename = filename

    def createFile(self):
        '''
        Creates the in-memory data structure.
        Note the actual file creation happens in closeFile().
        '''
        self.root = etree.Element(self.rootTag)
        self.root.attrib['producer'] = FILE_PRODUCER
        self.root.attrib['file_time'] = FILE_TIMESTAMP
        self.root.attrib['file_name'] = self.filename
        #self.root.attrib['Python_etree_version'] = etree.__version__
        self.root.attrib['svn_id'] = SVN_ID

    def closeFile(self):
        '''write (or overwrite) the named XML file'''
        if self.root is not None and self.filename is not None:
            text = etree.tostring(self.root, pretty_print=True, encoding='utf-8')
            f = open(self.filename, 'w')
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            #if xslt != None:
            #    f.write('<?xml-stylesheet type="text/xsl" href="%s"?>\n' % xslt)
            f.write( text )
            f.close()

    def createEntry(self, name):
        if self.root is None:
            raise "No parent SASroot node created yet!"
        self.entry = etree.SubElement(self.root, 'SASentry')
        self.entry.attrib['name'] = name        # TODO: automatically choose this name
        self.entry.attrib['version'] = CANSAS_VERSION
        self.sasdata = None

    def createTitle(self, title):
        if self.root is None:
            raise "No parent SASentry node created yet!"
        node = etree.SubElement(self.entry, 'Title')
        node.text = title
    
    def createData(self, name, qi, ii, otherattr=None):
        if self.entry is None:
            raise "No parent SASentry node created yet!"
        self.sasdata = etree.SubElement(self.entry, 'SASdata')
        self.sasdata.attrib['name'] = name        # TODO: automatically choose this name
        self.sasdata.attrib['I_axes'] = ii
        items = self._list_to_text_list(qi)
        self.sasdata.attrib['Q_indices'] = items
        if otherattr != None:
            for key in otherattr.keys():
                 self.sasdata.attrib[key] = otherattr[key]

    def createDataSet(self, name, array, attributes=None):
        if self.sasdata is None:
            raise "No parent SASdata node created yet!"
        node = etree.SubElement(self.sasdata, name)
        text = self._list_to_text_list(array.shape, delimiter='')
        node.attrib['size'] = text.strip('(),')
        arrText = self._list_to_text_list(array, delimiter=' ')
        if len(array.shape)>1:      # multi-dimensional
            # split into lines on lowest index, 
            # blank lines between rectangular blocks for higher dimensionalities
            arrText = string.replace(arrText, ']', '\n')
            arrText = string.replace(arrText, '[', ' ')
            # indent all lines by the same amount
            arrText = '\n' + '\n'.join([' '*8 + line.strip() for line in arrText.splitlines()])
            arrText += '\n' + ' '*6
        node.text = arrText
        if attributes != None:
            for key, value in attributes.items():
                node.attrib[key] = value

    def _list_to_text_list(self, data, delimiter = ','):
        # FIXME: fails when len(data) > 1000, array is truncated
        # TODO: return _all_ content of long np arrays (no " ... " in the middle)
        return delimiter.join( str(data).strip('[]').split() )


