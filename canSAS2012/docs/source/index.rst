.. $Id$

==================================================
Description of the canSAS2012 data format
==================================================


Computing power has increased to the point where it is now possible to consider 
routinely analysing multi-dimensional small angle scattering data. This is of 
particular value when considering non-azimuthally symmetric data from ordered 
systems and for the grazing incidence SAS experiments. 

One of the first aims of the canSAS [#]_ (Collective Action for Nomadic Small-Angle 
Scatterers) forum of users and facility staff was to discuss better sharing of 
SAS data analysis software. One means of doing so is through common data formats 
to allow the easy use of different analysis software packages. Having developed 
an XML based standard for one-dimensional reduced small-angle scattering data, [#]_ 
which is in use at multiple facilities, we now present a framework for storage of 
reduced multi-dimensional data. This not only includes the common concept of 
storing image data from the detector in 2 dimensions but also adding dimensions 
for parameters that were varied during the experiment (pressure, concentration,
temperature, etc.). This is done in a way so the analysis program can take this 
into account.

The targeted reduced data should be free from any correctable instrumental 
effects. We identified the absolute minimum required data objects for analysis, 
a standard recommended set and a dictionary of optional terms for various 
types of experiments. The devised hierarchical storage structure is in principle 
agnostic to the container format. With data of rank 2 and higher we recommend 
HDF5 as an efficient container and that is what the reference examples are 
provided for.

The format is still in the consultation and evaluation phase. 
We present the details of the data format and some examples of usage 
and welcome comments.

	The canSAS (Collective Action for Nomadic Small-Angle Scatterers) forum 
	met in Uppsala, Sweden in July 2012 [#]_ to discuss standardization of the 
	storage of reduced small-angle scattering of any dimension to be considered 
	for analysis. [#]_
	
	This document describes the current specification as an 
	outcome of that meeting.


.. toctree::
   :maxdepth: 2
   
   contents

---------------------

.. rubric:: Footnotes

.. [#]	http://www.cansas.org
.. [#]	http://svn.smallangles.net/trac/canSAS/browser/1dwg/tags/v1.0/doc/cansas-1d-1_0-manual.pdf
.. [#]  http://www.smallangles.net/wgwiki/index.php/canSAS-2012
.. [#]  http://www.smallangles.net/wgwiki/index.php/2012_Data_Discussion
