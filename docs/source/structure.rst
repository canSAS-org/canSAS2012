.. $Id$

.. _Structure:


=====================================================
Structure of the canSAS2012 data format
=====================================================

make some brief comments about this structure

Note:

.. _name note:

* Name attributes are allowed to be chosen by the data file writer.
  However, a `name` must adhere to the :ref:`naming standard <naming standard>` 
  for `name` attributes **and** must be unique within the containing group.
  
  .. TODO: this remark would be better placed in the hdf5.rst file.  
     It's out of place and distracting here.
  
  In some file containers, such as HDF5, the names of items in each group 
  must be unique.  To write the canSAS standard in HDF5/NeXus, use the `@name` 
  attribute of a group as the group's HDF5 name.  Write the type as
  the @NX_class attribute and replace the "`SAS`" letters with '`NX`"
  in the group type.  More on this in the HDF5 implementation
  titled: :ref:`hdf5_implementation`.  Here's an example in HDF5:

  .. code-block:: text
	  :linenos:
	  
	  SASroot
	    @NX_class = "NXroot"
	    sasentry01
	      @NX_class = "NXentry"
  

* `@` prefix is a notation in this documentation that means the named item is an attribute.  
  When used, do not actually use the `@` symbol.
  
* Occurrence describes how many times a particular item is allowed to or must appear.
  We use a notation of `[s..f]`.  The `s` term indicates the minimum number of times 
  the item is required to appear (where `0` means optional and `1` means required).  
  The `f` term indicates the maximum number of times the item is allowed to appear 
  (where `inf` means unlimited).

  ========== =========================================================
  notation   meaning
  ========== =========================================================
  `[0..1]`   the item is optional but may appear only once, if at all
  `[1..1]`   the item is required and must appear only once
  `[1..inf]` the item is required and may appear one or more times
  ========== =========================================================

* Within each group, the order in which each item appears is not important.



.. index:: ! SASroot, groups; SASroot

.. _SASroot:

SASroot
===========

The **SASroot** group is the beginning of the canSAS structure.  It is used to 
hold the data from one or more experiments, contained in one or more 
:ref:`SASentry <SASentry>` groups.

In an HDF5 file, it is not necessary to create this group but rather, one should
use the root of the HDF file as the **SASroot** group.

=============== ================= ============ =================================================================
Name            Type              Occurrence   Description
=============== ================= ============ =================================================================
@file           string            [1..1]       original data file name
@time           string            [1..1]       date and time (ISO 8601 format) that this file was written
:ref:`SASentry` group             [1..inf]     Each **SASentry** group contains the data (SAS and analysis) 
                                               pertaining to measurements of a single sample. 
=============== ================= ============ =================================================================

This is an example of the **SASroot** group (subgroup information not shown)

.. sidebar::  TODO:
   
   This example could be improved.
   Such as the filename and the name of the `time` attribute.

.. code-block:: text
  :linenos:
  
  SASroot
    @file = "/home/pi/data/cansas-demo.dat"
    @time = "2012-12-28 11:58:47 CST"
    SASentry
      @name = "sasentry01"


.. index:: ! SASentry, groups; SASentry

.. _SASentry:

SASentry
===========

A single SAS scan is reported in a **SASentry**. Include as many
**SASentry** elements as desired.  They may contain related or
unrelated data.  Other items may be added to a **SASentry** group
but these may be ignored by analysis or visualization software.

===================== ============ ============ =================================================================
Name                  Type         Occurrence   Description
===================== ============ ============ =================================================================
@name                 string       [1..1]       Unique identifier of this entry group.  
                                                See the :ref:`name note <name note>` above.  
                                                Example::
                                            
                                            		@name="sasentry01"
@version              string       [0..1]       Specific version of the canSAS standard used to write 
                                                this data.  This **must** be a text (not numerical) 
                                                representation.  Example::
                                            
                                            		@version="2.0"
Title                 string       [0..1]       Description of this entry.  Example::
                                            
                                            		Title = "Glassy Carbon C4 12keV"
:ref:`SASdata`        group        [1..inf]     The reduced :math:`I(Q)` SAS data.
                                            
                                                Each **SASdata** group contains the reduced SAS data
                                                from measurements of a single sample.
                                                Use multiple **SASdata** elements to 
                                                represent multiple :math:`I(Q)` measurements.
:ref:`SASsample`      group        [0..1]       Information about this sample.
:ref:`SASinstrument`  group        [0..1]       Information about the instrument that measured this data.
:ref:`SASprocess`     group        [0..inf]     Description of a processing or analysis step.
:ref:`SASnote`        group        [0..inf]     Free form description to describe anything not already described.
===================== ============ ============ =================================================================

This is an example of the **SASentry** group (subgroup information not shown)

.. code-block:: text
  :linenos:
  
  SASentry
    @name = "sasentry01"
    @version = "2.0"
    Title = "Glassy Carbon C4 12keV"
    SASdata
      @name = "sasdata01"
    SASsample
      @name = "sample"
    SASinstrument
      @name = "sasinstrument01"
    SASprocess
      @name = "sasprocess01"
    SASnote
      @name = "sasnote01"


.. index:: ! SASdata, groups; SASdata

.. _SASdata:

SASdata
===========

Contains the reduced data :math:`I(Q)` for analysis from a single SAS measurement.
The table below shows the terms that are defined as part of the canSAS standard.
Additional terms may be specified, as indicated in the section titled :ref:`SASdata discussion`.

.. note:: For all numerical quantities, a :ref:`units <units>` attribute is required.

===================== ============ ============ =================================================================
Name                  Type         Occurrence   Description
===================== ============ ============ =================================================================
@name                 string       [1..1]       Unique identifier of this data group.  
                                                See the :ref:`name note <name note>` above.  
                                                Example::
                                            
                                            		@name="sasdata01"
@Q_indices            string array [1..1]       Describes which indices of `I` provide `Q`-related data.
@I_axes               string array [1..1]       Tells the names of the datasets for `I` for each index position.
@Mask_indices         string array [1..1]       Describes which indices of `I` provide `Mask`-related data.
Q                     float        [1..1] [#]_  :math:`|Q|`, as defined  in :ref:`Q scalar`.
Qx                    float        [1..1]       :math:`\vec Q \cdot \hat x`, as defined  in :ref:`Q vector`.
Qy                    float        [1..1]       :math:`\vec Q \cdot \hat y`, as defined  in :ref:`Q vector`.
Qz                    float        [1..1]       :math:`\vec Q \cdot \hat z`, as defined  in :ref:`Q vector`.
I                     float        [1..1]       The reduced SAS intensity data, as defined in :ref:`I`.
Mask                  int          [0..1]       Array (same shape as `I`) that indicates which values of the
                                                `I` array should be used for analysis.  (1 = use, 0 = ignore)
probe_type            string       [0..1]       Name of the radiation used. 
                                                For maximum compatibility with NeXus, use one of these strings
                                                as defined in the NeXus **NXsource** definition for `type` 
                                                or `probe`: [#]_
                                                
                                                * Spallation Neutron Source
                                                * Pulsed Reactor Neutron Source
                                                * Reactor Neutron Source
                                                * Synchrotron X-ray Source
                                                * Pulsed Muon Source
                                                * Rotating Anode X-ray
                                                * Fixed Tube X-ray
                                                * neutron
                                                * x-ray
                                                * muon
                                                * electron
wavelength            float        [0..1]       Wavelength of the incident radiation.  May be a scalar or an array.
transmission          float        [0..1]       Sample transmission.  May be a scalar or an array.
:ref:`SASnote`        group        [0..inf]     Free form description to describe anything not already described.
===================== ============ ============ =================================================================

.. [#] 	Either `Q` must be present or `Qx`, `Qy`, and `Qz` must all be present.
.. [#] 	NeXus **NXsource**: http://download.nexusformat.org/doc/html/classes/base_classes/NXsource.html

This is an example of the **SASdata** group (subgroup information not shown)

.. code-block:: text
  :linenos:
  
  SASdata
    @name = "sasdata01"
    @Q_indices = 0 
    @I_axes = Q
    Q: float[]
      @units = "1/A"
    I: float[]
      @units = "1/cm"
      @uncertainty = "Idev"
    Idev: float[]
      @units = "1/cm"
    probe_type = "x-ray"
    wavelength = 1.0401
      @units = "A"

@Q_indices
----------------

Array attribute that describes which indices (of the `I` data object) are 
used to reference `Q`. The items in this array use zero-based indexing.

@I_axes
----------------

String array that describes the names of the data objects that 
correspond to the indices of the I object. 

@Mask_indices
----------------

Array attribute that describes which indices (of the `I` data object) are 
used to reference `Mask`. The items in this array use zero-based indexing. 

Mask
---------------

TODO: show how to use the mask and how NOT to use the mask

The point of the mask is to indicate which intensity values should be considered
for analysis (value = 1) and which should be ignored (value = 0).  To preserve
the statistics, masking is a procedural operation, **not** a mathematical operation.

Example with multi-dimensional :math:`I(Q)`
---------------------------------------------

.. sidebar::  Compare with these examples:

   * :ref:`example 2-D.images.with.varied.T.t.P`
   * :ref:`example 2-D masked image`


Consider an example case of :math:`I(T,t,P,Q(t))` where the intensity is a function of
temperature, time, pressure, and :math:`Q`, respectively.  Also, in this hypothetical
case, the intensity was recorded on a two-dimensional grid of 100,512 size, including intensity 
uncertainties, and some of the grid must be masked to remove it from consideration 
for analysis.  Thus, the intensity is a 5-dimensional array::

	@I_axes=Temperature,Time,Pressure,Q,Q

This specifies two types of information.  First, this specifies the index positions
for the various related data.  Second, this specifies the names of the related datasets.
`Temperature` varies in the first index, `Time in the second, `Pressure` in the third, 
and 2-D :math:`Q` in the last two indices.
In this particular case, since :math:`Q` is also a function of time, we specify::

	@Q_indices = 1,3,4

where `1` indicates the position of the time index (second position) 
and `3,4` indicate the positions of the 2-D grid indices.
As a final permutation, the mask was not a function of time for some reason
but only a function of :math:`Q`, so that::

	@Mask_indices = 3,4

Putting this all together, with accompanying datasets:

.. caution:: TODO: Check this example!

.. code-block:: text
  :linenos:
  
  SASdata
    @name = "sasdata01"
    @Q_indices = 1,3,4 
    @I_axes = Temperature,Time,Pressure,Q,Q
    @Mask_indices = "3,4" 
    Qx: float[nTime,100,512]
      @units = "1/A"
    Qy: float[nTime,100,512]
      @units = "1/A"
    Qz: float[nTime,100,512]
      @units = "1/A"
    I: float[nTemperature,nTime,nPressure,100,512]
      @units = "1/cm"
      @uncertainty = "Idev"
    Idev: float[nTemperature,nTime,nPressure,100,512]
      @units = "1/cm"
    Mask: int[100,512]
    Temperature: float[nTemperature]
      @units = "K"
    Time: float[nTime]
      @units = "s"
    Pressure: float[nPressure]
      @units = "MPa"



.. index:: ! SASsample, groups; SASsample

.. _SASsample:

SASsample
===========

Note that `transmission` has been moved to the :ref:`SASdata` group.

===================== ============ ============ =================================================================
Name                  Type         Occurrence   Description
===================== ============ ============ =================================================================
@name                 string       [1..1]       Unique identifier of this sample group.  
                                                See the :ref:`name note <name note>` above.  
                                                Example::
                                            
                                            		@name="sample"
Title                 string       [0..1]       Description of this sample.  Example::
                                            
                                            		Title = "Glassy Carbon C4 12keV"
thickness             float        [0..1]       Thickness of this sample.
temperature           float        [0..1]       Temperature of this sample.
position              group        [0..1]       Translation position of this sample.
orientation           group        [0..1]       Rotational orientation of this sample.
details               string       [0..1]       Any additional sample details::
                                            
                                            		details = "obtained from the XYZ Company, batch #123456.7890"
===================== ============ ============ =================================================================




.. index:: ! SASinstrument, groups; SASinstrument

.. _SASinstrument:

SASinstrument
==============

Since the canSAS standard is intended to describe *reduced* small-angle scattering data,
the need for an elaborate **SASinstrument** group is minimal.  Indeed, this group is here 
merely for compatibility with instrumental descriptions of the raw data and is not necessary
for routine small-angle scattering data analysis.


.. index:: ! SASnote, groups; SASnote

.. _SASnote:

SASnote
===========

A **SASnote** group may contain any information.  The contents of **SASnote**
are left unspecified by the canSAS standard.  It is used to specify additional
information that has no specified place in the canSAS standard.


.. index:: ! SASprocess, groups; SASprocess

.. _SASprocess:

SASprocess
===========

Parameters used in processing or determined as a result of processing may 
be stored either in **SASnote** groups or in individual datasets.  
The names must adhere to the :ref:`naming standard <naming standard>` 
for `name` attributes **and** must be unique within the containing group.

===================== ============ ============ =================================================================
Name                  Type         Occurrence   Description
===================== ============ ============ =================================================================
@name                 string       [1..1]       Unique identifier of this process group.  
                                                See the :ref:`name note <name note>` above.  
                                                Example::
                                            
                                            		@name="sasprocess01"
Title                 string       [0..1]       Description of this processing step.  Example::
                                            
                                            		Title = "Irena regularization analysis"
date                  string       [0..1]       Optional date for this data processing or analysis step. 
                                                The date is to be written in the ISO-8601 format.  [#iso8601]_
                                                Example::
                                            
                                            		date = "2012-12-28 11:59:41 CST"
description           string       [0..1]       Optional description for this data processing or analysis step. 
                                                Example::
                                            
                                            		description = "first try at analysis"
:ref:`SASnote`        group        [0..inf]     Free form description to describe anything not already described.
===================== ============ ============ =================================================================

.. [#iso8601] ISO-8601 is a format for the date which is easily machine-readable
   (either yyyy-mm-ddThh:mm:ss or yyyy-mm-dd hh:mm:ss). 
   See: http://www.w3.org/TR/NOTE-datetime or 
   http://en.wikipedia.org/wiki/ISO_8601 for more details.


