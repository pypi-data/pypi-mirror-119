##########################
Spreadsheet
##########################

.. note::
   Many restrictions mentioned here will be removed in future as GUI is made more interactive


****************
Format
****************

- Currently, following are supported:

  1. Tab-separated values (tsv)
  2. comma-separated values (csv)

- First 2 or 3 columns are displayed with '`Truncated columns`' view.
- All values are assumed to be decimal numbers.


.. tabbed:: tsv

   .. code-block::
      :caption: natural_numbes.tsv

      	self	add2	power2	multiply2
      DP0	0	2	0	0
      DP1	1	3	1	2
      DP2	2	4	4	4
      DP3	3	5	9	6
      DP4	4	6	16	8
      DP5	5	7	25	10
      DP6	6	8	36	12
      DP7	7	9	49	14
      DP8	8	10	64	16
      DP9	9	11	81	18
      DP10	10	12	100	20
      DP11	11	13	121	22

.. tabbed:: csv

   .. code-block::
      :caption: natural_numbes.csv

      ,self,add2,power2,multiply2
      DP0,0,2,0,0
      DP1,1,3,1,2
      DP2,2,4,4,4
      DP3,3,5,9,6
      DP4,4,6,16,8
      DP5,5,7,25,10
      DP6,6,8,36,12
      DP7,7,9,49,14
      DP8,8,10,64,16
      DP9,9,11,81,18
      DP10,10,12,100,20
      DP11,11,13,121,22
