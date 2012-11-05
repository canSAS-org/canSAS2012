.. $Id$

.. index:: 
	! HDF5
	implementation; HDF5

.. _hdf5_implementation:

==================================================
Binary: HDF5
==================================================

.. sidebar:: work in progress...

	This document is under construction.
	Many parts have yet to be written.

It is expected that small-angle scattering data will be stored in 
binary HDF5 files (http://www.hdfgroup.org/HDF5/).  
To store SAS data in text files, see the chapter titled 
:ref:`xml_implementation`.

The basic plan here is to describe the implementation of 
the canSAS multi-dimensional format within the NeXus HDF5 format 
(http://www.nexusformat.org) by creating a new NeXus 
:index:`NXcansas` application definition, expressed as a 
NXDL file (http://download.nexusformat.org/doc/html/nxdl.html).  

The effort to create this NXDL definition will commence once 
the basics of the canSAS multi-dimensional format are set forth.

Contents:

.. toctree::
   :maxdepth: 2

