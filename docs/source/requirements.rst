.. $Id$

.. _requirements:

==================================================
Requirements 
==================================================

The absolute minimum information required for the standard 
analysis of small-angle scattering measurements is intensity 
as a function of scattering vector, :math:`I(\vec{Q})`.

* Allow for representation of *reduced data* of any dimensionality

  * 1D SAS data
  * 2D SAS data from detectors
  * additional dimensions for complex experiments
  * *Q* can be either a vector (:math:`\vec{Q}`) or a vector magnitude (:math:`|\vec{Q}|`)
* Identify and associate scanning axes
* Provide (when possible)

  * uncertainties and their constituents
  * masking information
* Allow for 

  * complex experiments with multiple detectors
  * easy plotting of the data in close to their raw form
* Maintain the original dimensionality of the data if at all possible
* Use existing standards where possible or practical
