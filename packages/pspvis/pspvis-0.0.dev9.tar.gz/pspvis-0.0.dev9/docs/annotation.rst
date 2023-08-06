####################
Annotation File
####################

Annotation file is in `yaml <https://yaml.org/spec/>`__ or `toml <https://toml.io/>`__
format.

************
Structure
************

Controlled keys:
==================

Three **case-sensitive** keys are necessary:

COLUMNS:
-----------
- Type: List
- **Contents**: Names of columns annotated by this annotation file (meta-data)

ROWS:
----------
- Type: List
- **Contents**: Names of rows annotated by this annotation file (meta-data)

SCHEMES:
-------------
- Type: Mapping object (Dict)
- **Contents**: <scheme_name>: ``schemes``

``scheme``
^^^^^^^^^^^^^
- Type: Iterable
- **Contents**: <group_name>: [List of (row|column) names belonging to group]
- **Contents**: <block> [List of (row|column) names belonging to group]

  If contents are <block>, then it is named by its occurrence index


Example:
==========

.. code:: yaml
  :name: ${HOME}/.config/pspvis.yml

   COLUMNS:
     self: independent
     add2: additive
     multiply2: multiplicative
     power2: exponential

   ROWS:
     DP0: zero
     DP1: one
     DP2: two
     DP3: three
     DP4: four
     DP5: five
     DP6: six
     DP7: seven
     DP8: eight
     DP9: nine
     DP10: ten
     DP11: eleven

   SCHEMES:
     impact:
     -
       - self
       - add2
       - multiply2
     -
       - power2
     oddeven:
       odds:
       - DP1
       - DP3
       - DP5
       - DP7
       - DP9
       - DP11
       even:
       - DP0
       - DP2
       - DP4
       - DP6
       - DP8
       - DP10
     squares:
       perfect:
       - DP0
       - DP1
       - DP4
       - DP9
       non:
       - DP2
       - DP3
       - DP5
       - DP6
       - DP7
       - DP8
       - DP10
       - DP11
     prime_factors:
       2:
       - DP0
       - DP2
       - DP4
       - DP6
       - DP8
       - DP10
       3:
       - DP0
       - DP3
       - DP6
       - DP9
       5:
       - DP0
       - DP5
       - DP10
       7:
       - DP0
       - DP7
       11:
       - DP0
       - DP11
