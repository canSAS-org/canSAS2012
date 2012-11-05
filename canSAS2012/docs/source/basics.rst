.. $Id$

==================================================
Definitions
==================================================

.. sidebar:: work in progress...

	This document is under construction.
	Many parts have yet to be written.

For the general case of small-angle scattering data, all that is required is
to have measurements of reduced intensity :math:`I` as a function scattering 
vector, :math:`Q`.  Some techniques may require additional information, such 
as wavelength.

.. index:: ! reduced data

.. _reduced data:

Reduced Data
=========================

What is *reduced data*?  Consider this figure of the scientific workflow 
presented at the 
*2006 Advanced Photon Source Workshop on Scientific Software* 
(*ANL-APS-TB-51*, Argonne National Laboratory):
	
	.. figure:: graphics/2006-10-09-scientific-workflow.jpg
	    :alt: scientific workflow
	    :height: 400 px

.. note:: *Reduced data* is the data presented for analysis after all 
	instrument-specific artifacts and corrections have been applied.

An *experiment* is constructed from a sequence of *measurements* by a scientific
instrument.  Raw data from those measurements must be converted from the format 
received by components of the instrument (detectors, amplifiers, motors, encoders, 
thermocouples, etc.) into a form suitable for analysis particular 
to the scientific investigation.  Part of the conversion process involves the removal of
artifacts and the correction of distortions of the signal by the measurement process
(such as detector dead-time corrections or removal of dead pixels from an area 
detector image) and the combination of parameters describing the instrument configuration
and even the possibility of an applied mask to remove parts of the measurement
that contain no useful observations.  
The data that results after all these conversion steps have 
been applied is termed **reduced data**.

In broad terms, the steps involved in the process of data reduction are 
particular to a specific scientific instrument as it existed at a specific 
time.  For many scientific instruments, such as those at large user facilities,
it is not possible to generalize the process of data reduction and identify
all the parameters necessary for data reduction in advance.  
	
.. note:: It is, and will always be, the responsibility of the instrument team 
	to provide the process of converting the data measurements into
	**reduced data**.

Requirements for Reduced SAS Data
----------------------------------------------

The absolute minimum information required for the standard analysis 
of small-angle scattering measurements is intensity as a function of 
scattering vector, :math:`I(Q)`.

:ref:`Intensity <I>`
	is expressed in absolute units of cross-section 
	or in units directly convertible by a scaling constant

:ref:`scattering vector <Q>`
	is expressed as :ref:`scattering vector 
	magnitude <Q scalar>` (:math:`|Q|`) 
	or :ref:`scattering vector  <Q vector>` (:math:`\vec{Q}`)

Some analyses may require additional information such as
the estimation of experimental uncertainties, the
wavelength and type of the radiation probe,
or the instrumental resolution.  These should be provided,
where possible.  Note that, for example, reduced SAS data does not
*require* a number representing the distance from sample to detector as this
common instrument-specific term has already been factored into the data 
reduction process.

.. index:: ! Q

.. _Q:

Definition of :math:`Q`
=========================

:math:`Q` may be represented either as the magnitude of the scattering vector,
:math:`|Q|` or by the three-dimensional scattering vector :math:`\vec{Q}`.
When we write :math:`Q`, we may refer to either or both of :math:`|Q|` 
or :math:`\vec{Q}`,  depending on the context.

.. _Q scalar:

Q vector magnitude: :math:`|Q|=(4 \pi / \lambda) \sin(\theta)`
------------------------------------------------------------------

	where :math:`\lambda` is the wavelength of the radiation,
	and :math:`2\theta` is the angle through which the detected radiation has been scattered.
	This is a one-dimensional reduction of the general case below.
	
	.. _Q geometry:
	
	.. figure:: graphics/Q-geometry.jpg
	    :alt: Q geometry
	    :height: 200 px
	    
	    definition of :math:`|Q|` geometry for small-angle scattering



.. _Q vector:

Q vector: :math:`\vec{Q}=\vec{k'}-\vec{k}`
----------------------------------------------

	where :math:`\vec{k}` is the wave vector of the incident radiation
	and :math:`\vec{k'}` is the wave vector of the scattered radiation.
	Here, :math:`\vec{k}` is a vector of magnitude :math:`2\pi/\lambda`
	that points along the trajectory of the radiation.
	
	.. _Q vector geometry:
	
	.. figure:: graphics/q-vector.png
	    :alt: Q vector geometry
	    :height: 400 px
	    
	    definition of :math:`\vec{Q}` geometry for small-angle scattering [#]_

.. [#] A hearty nod for this graphic is given to the guide:
	**neutron scattering: A Primer**, 
	by Roger Pynn (LANSCE), 
	published in the Summer 1990 edition of *Los Alamos Science*.



.. index:: ! I

.. _I:

Definition of Intensity: :math:`I`
==========================================

The intensity may be represented in one of these forms:

**absolute units**: :math:`d\Sigma/d\Omega(Q)`
	differential cross-section
	per unit volume per unit solid angle (typical units: 1/cm/sr)

**absolute units**: :math:`d\sigma/d\Omega(Q)`
	differential cross-section
	per unit atom per unit solid angle (typical units: cm^2)

**arbitrary units**: :math:`I(Q)`
	usually a ratio of two detectors 
	but units are meaningless (typical units: a.u.)

This presents a few problems 
for analysis software to sort out when reading the data.
Fortunately, it is possible to analyze the *units* to determine which type of
intensity is being reported and make choices at the time the file is read. But this is
an area for consideration and possible improvement.

One problem arises with software that automatically converts data into some canonical
units used by that software. The software should not convert units between these different
types of intensity indiscriminately.

.. index:: I(Q)

A second problem is that when arbitrary units are used, then the set of possible
analytical results is restricted.  With such units, no meaningful volume fraction 
or number density can be determined directly from :math:`I(Q)`.

In some cases, it is possible to apply a factor to convert the arbitrary 
units to an absolute scale.  This should be considered as a possibility 
of the analysis process.



.. index:: ! coordinate axes

.. _coordinate axes:

Coordinate Axes
===========================

The canSAS standard assumes a right-hand rule coordinate system, 
consistent with a variety of software packages and data formats.
See, for example: http://www.nexusformat.org/Coordinate_Systems

:z:
	:math:`z` is along the trajectory of the radiation
	(positive value in the direction towards the detector)
:x:
	:math:`x` is orthogonal to :math:`z` in the horizontal plane
	(positive values increase to the right when viewed 
	towards the incoming radiation)
:y:
	:math:`y` is orthogonal to :math:`z` and :math:`x` 
	in the vertical plane (positive values increase upwards)
		



.. index::
	! orientation
	roll
	pitch
	yaw

.. _orientation:

Orientation
===========================

Orientation (angles) describes single-axis rotations (rotations about
multiple axes require more information):
	
**roll**
	is a rotation about the :math:`z` axis

**pitch**
	is a rotation about the :math:`x` axis

**yaw**
	is a rotation about the :math:`y` axis
