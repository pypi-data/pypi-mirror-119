***************
Prerequisites
***************

- `Python3 <https://www.python.org/downloads/>`__ version >= 3.7
   - tkinter

********
Install
********

pip
====
Preferred method

Install
--------

.. tabbed:: pip

   .. code-block:: sh
      :caption: pip

      pip install pspvis

.. tabbed:: module import

   .. code-block:: sh
      :caption: if ``command not found: pip``

      python3 -m pip install pspvis


Update
-------
.. tabbed:: pip

   .. code-block:: sh
      :caption: pip

      pip install -U pspvis

.. tabbed:: module import

   .. code-block:: sh
      :caption: if ``command not found: pip``

      python3 -m pip install -U pspvis


Uninstall
----------

.. tabbed:: module import

   .. code-block:: sh
      :caption: pip

      pip uninstall -y pspvis

.. tabbed:: module import

   .. code-block:: sh
      :caption: if ``command not found: pip``

      python3 -m pip uninstall -y pspvis



`pspman <https://gitlab.com/pradyparanjpe/pspman>`__
=====================================================

(Linux only)

For automated management: updates, etc


Install
--------

.. code-block:: sh

   pspman -s -i https://gitlab.com/pradyparanjpe/pspvis.git



Update
-------

.. code-block:: sh

    pspman


*That's all.*


Uninstall
----------

Remove installation:

.. code-block:: sh

    pspman -s -d pspvis
