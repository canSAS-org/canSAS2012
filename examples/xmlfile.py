#!/usr/bin/env python

'''
Generate synthetic data to demonstrate canSAS (2012) data structure in XML

:see: http://www.smallangles.net/wgwiki/index.php/2012_Data_Discussion_Examples
'''

import string, os
from lxml import etree


class xmlfile():
    '''Support for creating and writing XML files (not reading)'''
    rootTag = "SASroot"
    root = None
    filename = None
    entry = None
    sasdata = None
    
    def __init__(self, filename, **keywords):
        self.filename = os.path.join("xml", filename + ".xml")
        self.keywords = keywords

    def createFile(self):
        '''
        Creates the in-memory data structure.
        Note the actual file creation happens in closeFile().
        '''
        self.root = etree.Element(self.rootTag)
        
        self.root.attrib['file_name'] = self.filename
        self.root.attrib['Python_etree_version'] = etree.__version__
        for keyw in ["file_time", "producer"]:
            if keyw in self.keywords:
                self.root.attrib[keyw] = self.keywords[keyw]

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
        self.entry.attrib['name'] = name
        self.entry.attrib['version'] = "1.0"
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
        self.sasdata.attrib['I_axes'] = self._list_to_text_list(ii)
        self.sasdata.attrib['Q_indices'] = self._list_to_text_list(qi)
        if otherattr != None:
            for key in otherattr.keys():
                 self.sasdata.attrib[key] = self._list_to_text_list(otherattr[key])

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
        # TODO: return _all_ content of long np arrays (no " ... " in the middle
        try:
            return delimiter.join(data) # string
        except:
            return delimiter.join( str(data).strip('[]').split() ) # numpy
