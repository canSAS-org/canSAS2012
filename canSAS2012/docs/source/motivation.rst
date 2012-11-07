.. $Id$

.. _motivation:

==================================================
Motivation
==================================================

* One canSAS motive: 

  * Provide better shared SAS data analysis software
* One means of doing so is through common data formats such as 

  * sasCIF, *J. Appl. Cryst.* (2000). **33**, 812-816
  * cansas1d/1.0, http://www.cansas.org/formats/canSAS1d/1.1/doc/
  * bio SAS draft requirements, http://journals.iucr.org/services/sas/

..

* For 2-D (and higher dimensionality), the job is harder
* Often, 2-D analysis software tries to start with raw data
* Data reduction steps are particular to the instrument
  **as it existed at one specific time**.

Thus, data reduction and data analysis are two different tasks.
The data reduction is based on the the details of a specific instrument
while the data analysis is based on the scientific principles to be evaluated.

	.. note:: It is, and will always be, the responsibility of the 
	   instrument team to provide the process of converting 
	   the data measurements into :ref:`reduced data`.


:ref:`Reduced data <reduced data>` is the data presented for analysis after 
all instrument-specific artifacts and corrections have been applied.
By declaring our objective to store *reduced small-angle scattering data*,
we establish a defined interface that clearly divides the roles.
An instrument team must assemble the measured data, apply corrections 
and adjustments, and then generate the reduced data.
Analysis code will expect to receive the reduced data on which to base its operations.


