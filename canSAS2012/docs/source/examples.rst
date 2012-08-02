.. $Id$

.. _examples:

.. TODO: reorganize this as I(Q), then I(Q,t), then ...

==================================================
Examples of the canSAS2012 data format
==================================================

Describe, in general, the examples.  Explain how they were created and 
what assumptions were involved.

.. rubric: List of key Examples

* `minimum recommended 1-D example`_


.. _1-D Examples:

1-D Examples
==========================

simple 1D SAS data: :math:`I(Q)`
---------------------------------------------------------------------------------------------------

.. code-block:: text
	:linenos:
	
	SASroot
		SASentry
			SASdata
				@Q_indices=0
				@I_axes="Q"
				I: float[100]
				Q: float[100]

Examples:  :download:`XML <../../examples/xml/simpleexamplefile.xml>` 	:download:`HDF5 <../../examples/hdf5/simpleexamplefile.h5>`

An implementation of this structure in XML using the minimum recommended metadata is:

	.. _minimum recommended 1-D example:
	.. rubric:  1-D example using (the intensity standard) glassy carbon data and the minimum recommended metadata
	.. literalinclude:: example-1d.xml
	    :tab-width: 4
	    :linenos:
	    :language: xml

simple 1D SAS data in a time series: :math:`I(Q, t)`
---------------------------------------------------------------------------------------------------

.. code-block:: text
	:linenos:
	
	SASroot
		SASentry
			SASdata
				@Q_indices=1
				@I_axes="Time,Q"
				I: float[nTime,100]
				Q: float[100]
				Time: float[nTime]

Examples:  :download:`XML <../../examples/xml/simple1dtimeseries.xml>` 	:download:`HDF5 <../../examples/hdf5/simple1dtimeseries.h5>`

generic 1D SAS data in a time series: :math:`I(Q(t), t)`
---------------------------------------------------------------------------------------------------

This example is slightly more complex, showing data where :math:`Q` is also time-dependent.

.. code-block:: text
	:linenos:
		
	SASroot
		SASentry
			SASdata
				@Q_indices=0,1
				@I_axes="Time,Q"
				I: float[nTime,100]
				Q: float[nTime,100]
				Time: float[nTime]


.. _2-D Examples:

2-D Examples
=========================

simple 2D (image) SAS data: :math:`I(Q)`
---------------------------------------------------------------------------------------------------

.. code-block:: text
	:linenos:
	
	SASroot
		SASentry
			SASdata
				@Q_indices=0,1
				@I_axes="Q,Q"
				I: float[100, 512]
				Qx: float[100, 512]
				Qy: float[100, 512]
				Qx: float[100, 512]

Examples:  :download:`XML <../../examples/xml/simple2dcase.xml>` 	:download:`HDF5 <../../examples/hdf5/simple2dcase.h5>`

simple masked 2D (image) SAS data: :math:`I(Q)`
---------------------------------------------------------------------------------------------------

.. code-block:: text
	:linenos:
	
	SASroot
		SASentry
			SASdata
				@Q_indices=0,1
				@I_axes="Q,Q"
				@Mask_indices=0,1
				I: float[100, 512]
				Qx: float[100, 512]
				Qy: float[100, 512]
				Qz: float[100, 512]
				Mask: int[100, 512]

Examples:  :download:`XML <../../examples/xml/simple2dmaskedcase.xml>` 	:download:`HDF5 <../../examples/hdf5/simple2dmaskedcase.h5>`

generic 2D SAS data: :math:`I(Q)`
---------------------------------------------------------------------------------------------------

Could use this model, for example, to describe data from multiple detectors (by listing individual 
pixels from all detectors retained after any masking).  Or, could describe data from one detector 
of any geometry.  This is the most flexible.

.. code-block:: text
	:linenos:
	
	SASroot
		SASentry
			SASdata
				@Q_indices=0
				@I_axes="Q"
				I: float[100*512]
				Qx: float[100*512]
				Qy: float[100*512]
				Qz: float[100*512]

Examples:  :download:`XML <../../examples/xml/generic2dcase.xml>` 	:download:`HDF5 <../../examples/hdf5/generic2dcase.h5>`

simple 2D SAS/WAS data: :math:`Isas(Q) & Iwas(Q)`
---------------------------------------------------------------------------------------------------

Consider the multi-technique experiment that produces 
small-angle and wide-angle scattering data images.  
The reduced data results in images as well.  
Each image might be described separately (see 
``[[2012_Data_Discussion_Examples#example_of_SAS_data_with_several_detectors.2C_I.28Q.29 
| example of SAS data with several detectors]]`` for an alternative).  
Here the SAS data image is 100 x 512 pixels.  
The WAS data (not covered by this canSAS standard) is 256 x 256 pixels.

.. code-block:: text
	:linenos:
		
	SASroot
		SASentry
			SASdata
				@name="sasdata"
				@Q_indices=0,1
				@I_axes="Q,Q"
				I: float[100, 512]
				Qx: float[100, 512]
				Qy: float[100, 512]
			SASdata
				@name="wasdata"
				@Q_indices=0,1
				@I_axes="Q,Q"
				I: float[256, 256]
				Qx: float[256, 256]
				Qy: float[256, 256]

2D SANS and 2D SAXS: :math:`I_n(Q) & I_x(Q)`
---------------------------------------------------------------------------------------------------

Consider the multi-technique experiment that produces 
small-angle neutron and X-ray scattering data. 
Here the SANS data image is 100 x 512 pixels and
the SAXS data is 256 x 256 pixels.

.. code-block:: text
	:linenos:
	
	SASroot
		SASentry
			SASdata
				@name="sans"
				@Q_indices=0
				@I_axes="Q"
				I: float[100*512]
				Qx: float[100*512]
				Qy: float[100*512]
			SASdata
				@name="saxs"
				@Q_indices=0
				@I_axes="Q"
				I: float[256*256]
				Qx: float[256*256]
				Qy: float[256*256]

2D with additional varied parameters
==========================================

generic 2D SAS data in a time series: :math:`I(Q,t)`
---------------------------------------------------------------------------------------------------

.. code-block:: text
	:linenos:
	
	SASroot
		SASentry
			SASdata
				@Q_indices=1
				@I_axes="Time,Q"
				I: float[nTime,100*512]
				Qx: float[100*512]
				Qy: float[100*512]
				Qz: float[100*512]
				Time: float[nTime]

Examples:  :download:`XML <../../examples/xml/generic2dtimeseries.xml>` 	:download:`HDF5 <../../examples/hdf5/generic2dtimeseries.h5>`

generic 2D SAS data in a time series: :math:`I(Q(t),t)`
---------------------------------------------------------------------------------------------------

This example is slightly more complex, showing data where :math:`Q` is also time-dependent.

.. code-block:: text
	:linenos:
	
	SASroot
		SASentry
			SASdata
				@Q_indices=0,1
				@I_axes="Time,Q"
				I: float[nTime,100*512]
				Qx: float[nTime,100*512]
				Qy: float[nTime,100*512]
				Qz: float[nTime,100*512]
				Time: float[nTime]

2D SAS data as images in a time series with a time-independent mask: :math:`I(Q(t),t)`
-------------------------------------------------------------------------------------------------------

This example explores a bit of complexity added to the previous example.

.. code-block:: text
	:linenos:
	
	SASroot
		SASentry
			SASdata
				@Q_indices=0,1,2
				@I_axes="Time,Q,Q"
				@Mask_indices=1,2
				I: float[nTime,100,512]
				Qx: float[nTime,100,512]
				Qy: float[nTime,100,512]
				Qz: float[nTime,100,512]
				Time: float[nTime]
				Mask: int[100,512]

generic 2D SAS data in a time, T, & P series: :math:`I(t,T,P,Q(t,T,P))`
---------------------------------------------------------------------------------------------------

Complex case where all :math:`Q` values are different for each of time, temperature, and pressure.

.. code-block:: text
	:linenos:
		
	SASroot
		SASentry
			SASdata
				@Q_indices=0,1,2,3
				@I_axes="Time,Temperature,Pressure,Q"
				I: float[nTime,nTemperature,nPressure,100*512]
				Qx: float[nTime,nTemperature,nPressure,100*512]
				Qy: float[nTime,nTemperature,nPressure,100*512]
				Qz: float[nTime,nTemperature,nPressure,100*512]
				Time: float[nTime]
				T: float[nTemperature]
				P: float[nPressure]

Examples:  :download:`XML <../../examples/xml/generic2dtimetpseries.xml>` 	:download:`HDF5 <../../examples/hdf5/generic2dtimetpseries.h5>`

generic 2D SAS data (images) in a time, T, & P series: :math:`I(T,t,P,Q(t))`
---------------------------------------------------------------------------------------------------

Slightly less complex than previous, where :math:`Q` only depends on time.

.. code-block:: text
	:linenos:
	
	SASroot
		SASentry
			SASdata
				@Q_indices=1,3,4
				@I_axes="Temperature,Time,Pressure,Q,Q"
				I: float[nTemperature,nTime,nPressure,100,512]
				Qx: float[nTime,100,512]
				Qy: float[nTime,100,512]
				Qz: float[nTime,100,512]
				Time: float[nTime]
				Temperature: float[nTemperature]
				Pressure: float[nPressure]

SAS data with several detectors: :math:`I(Q)`
---------------------------------------------------------------------------------------------------

Here, the data are appended to common data objects.
This hypothetical case has reduced data derived from 
three detectors, Ia(Q), Ib(Q), and Ic(Q):
* Ia(Q) is derived from a 2D detector (100 x 512 pixels)
* Ib(Q) is derived from a 1D detector (2000 pixels)
* Ic(Q) is derived from a 2D detector (256 x 256 pixels)

Data from a SAXS/MAXS/WAXS instrument might be represented thus.

.. code-block:: text
	:linenos:
		
	SASroot
		SASentry
			SASdata
				@Q_indices=0
				@I_axes="Q"
				I: float[100*512  + 2000 + 256*256]
				Qx: float[100*512 + 2000 + 256*256]
				Qy: float[100*512 + 2000 + 256*256]
				Qz: float[100*512 + 2000 + 256*256]

----------

.. TODO: Could make this a note

Invalid Case
======================

Over-simplified 2D (image) SAS data: :math:`I(Q)`
---------------------------------------------------------------------------------------------------

Invalid because the method of addressing the Q values 
is different from all the above.

.. code-block:: text
	:linenos:
		
	SASroot
		SASentry
			SASdata
				@Q_indices="*,*"
				@I_axes=" ??? "
				I: float[100, 512]
				Qx: float[100]
				Qy: float[512]


Terms
===============

SASroot:
	same use as original 1D format
SASentry:
	some changes from the original 1D format

	needs a ''version'' attribute that describes the version of the 
	canSAS definition of SASentry.  Use: ``version="1.0"``

SASdata:
	different use from original 1D format, refers to a single
	reduced data set that can be represented thus (such as
	from one detector)

	:attribute I_axes: Comma-separated list that describes the names 
							of the data objects that correspond to the 
							indices of the ``I`` data object.  Such as::
							
								@I_axes="Temperature,Time,Pressure,Q,Q"
	:attribute Q_indices: Array that describes which indices 
							(of the :math:`I` data object) are used to 
							reference the ``Q`` data object. The items in this array 
							use zero-based indexing.  Such as::
							
								@Q_indices=1,3,4
							
							which indicates that Q requires three indices
							from the :math:`I` data object: one for time and
							two for Q position. 
	:attribute Mask_indices: Array that describes which indices
							(of the :math:`I` data object) are used to 
							reference the ``Mask`` data object.  The items in this
							array use zero-based indexing.  Such as::
							
								@Mask_indices=3,4
							
							which indicates that Q requires two indices
							from the :math:`I` data object for Q position. 
	
	To indicate the dependency relationships of other varied parameters, 
	use attributes similar to ``@Mask_indices`` (such as ``@Temperature_indices``
	or ``@Pressure_indices``).

..
	SASdata has some possible attributes, as shown in this example:
	
	<pre>
	@Q_indices=1,3,4
	@I_axes="Temperature,Time,Pressure,Q,Q"
	@Mask_indices=3,4
	</pre>
	
	To indicate the dependency relationships of other varied parameters, use attributes similar to ''@Mask_indices'' (such as ''@Temperature_indices'' or ''@Pressure_indices'').
	
	=== @Q_indices ===
	Array attribute that describes which indices (of the I data object) are used to reference Q.
	The items in this array use zero-based indexing.
	
	=== @I_axes ===
	Comma-separated list that describes the names of the data objects that correspond to the indices of the I object.
	
	=== @Mask_indices ===
	Array attribute that describes which indices (of the I data object) are used to reference Mask.
	The items in this array use zero-based indexing.

Algorithm for Software to Read Data files Written with this Structure
======================================================================

to be written

..
	Contents:
	
	.. toctree::
	   :maxdepth: 2

..
	.. code-block:: text
	    :linenos:

	.. literalinclude:: ../markup_example/hkl_ioc.mac.original
	    :tab-width: 4
	    :linenos:
	    :language: guess

	.. figure:: example1.png
	    :alt: view of original hkl_ioc.mac HTML documentation
	
	    Documentation of the original **hkl_ioc.mac** file.


