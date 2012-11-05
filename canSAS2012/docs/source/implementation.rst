.. $Id$

.. index:: ! implementation

.. _implementation:

==================================================
Implementation(s) of the canSAS2012 data format
==================================================

Describe why we have multiple implementations (small data community demands simple, 
readable text while large data community demands efficient binary storage).
Describe that canSAS must let the community decide.  (Largely based on the 
decisions of data suppliers and analysis software creators.)
Describe here some general information about the implementation(s).
Describe what is common amongst the implementations and what is not.

Contents:

.. toctree::
   :maxdepth: 2
   
   xml
   hdf5

.. need to describe the algorithms and software to read this format



Algorithm for Software to Read Data files Written with this Structure
======================================================================

#. open the file and read the *SASroot* (or root-level) group.
#. open each *SASentry* group:
	#. verify the version attribute: must be "1.0" (a string)
	#. note the *name* attribute, if present
	#. note the title, if present
	#. note the *SASsample* group contents, if present
	#. open each *SASdata* group
		#. note the *name* attribute, if present
		#. read the *I_axes* attribute, it tells the names (in storage order) of the other data objects on which *I* depends.
		#. read the *Q_indices* attribute, it tells which of the *I_axes* (zero-based numbering) have *Q* dependence
		#. if present, read the *Mask_indices* attribute (similar to the ``Q_indices``), to get the dependencies of the ``Mask``.
		#. read ``I`` data object as described below (see `Read a data object`_)
		#. same for ``Q``, ``Qx``,  ``Qy``,  ``Qz`` data objects (if present)
		#. same for the names in the *I_axes* attribute (except for *Q* since it was already handled)


.. _Read a data object:
.. rubric:: Read a data object

#. read the *size* attribute, if present
#. allocate memory for the object
#. read the data object and its units
#. if present, read the *uncertainty* attribute and read the named data object it describes



Algorithm to Identify :math:`Q` values given a set of indices on the ``I`` data
===============================================================================

Given an intensity data object (called ``I``), the algorithm to identify the associated
``Q`` values with any given intensity datum is described here:

#. Identify the given set of indices with the names of data objects
	#. note the set of indices for the intensity datum
	#. note the names of the various intensity axes from the ``I_axes`` attribute
#. note the list of indices for *Q* as given by the ``Q_indices`` attribute
#. ... this gets tedious without a couple examples...
#. analyze how we do it below and finish writing this part

.. caution:: This write-up is unfinished at this point.  Follow below for a few examples.

simple time-series example
--------------------------

.. sidebar:: Simplified example

	To simplify our example, only the relevant metadata has
	been left in this example.

Consider the SAS data example including a time-series (same model as :ref:`2-D I(t,Q(t))`):

	.. code-block:: text
		:linenos:
		
		SASroot
		  SASentry
		    SASdata
		      @name="sasdata01"
		      @I_axes="Time,Q"
		      @Q_indices=0,1
		      Qx : float[4,35]
		      Qy : float[4,35]
		      Qz : float[4,35]
		      I : float[4,35]
		      Time : float[4]

	#. The *I_axes* attribute describes a *Time* data object, in addition to some *Q* data.  The *Time* index is in the first position.
	#. It also says that there is only one index to use (the second index on intensity) when looking up a :math:`Q` value.
	#. Since there is no *Q* data object, there must be three data objects *Qx*, *Qy*, *Qz* that provide the scattering vector.
	#. The *Q_indices* attribute indicates that the lookup of *Q* depends on both the *Time* (0) and *Q* (1) indices and that *Q* is time-dependent.
	#. One index (position 0) is used to lookup the *Time* value.
	#. index *i* is for *Time* and index *j* is for *Q*.
	
	Given the indices ``i,j``, return all the data for this datum::
	
		Qx[i,j], Qy[i,j], Qz[i,j], Time[i], I[i,j]


simple time-series example
--------------------------

Consider the example of the 2-D time-dependent masked :ref:`image <2-D.time-dependent.masked.image>`.

	Given the indices ``i,j,k``, return all values for this datum::
	
		Qx[i,j,k], Qy[i,j,k], Qz[i,j,k], Time[i], Mask[j,k], I[i,j,k]


another example
--------------------------

See the model for 2-D  :math:`I(T,t,P,Q(t))` :ref:`images <2-D.images.with.varied.T.t.P>`.

	Given the indices ``i,j,k,l,m``, return all values for this datum::
	
		Qx[j,l,m], Qy[j,l,m], Qz[j,l,m], Temperature[i], Time[j], Pressure[k], I[i,j,k,l,m]




