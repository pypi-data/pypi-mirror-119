***************
Prerequisites
***************

- Python3
- pip

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
      :caption: install

      pip install <PROJECT>


.. tabbed:: module import

   .. code-block:: sh
      :caption: if ``command not found: pip``

      python3 -m pip install <PROJECT>


Update
-------

.. tabbed:: pip

   .. code-block:: sh
      :caption: install

      pip install -U <PROJECT>


.. tabbed:: module import

   .. code-block:: sh
      :caption: if ``command not found: pip``

      python3 -m pip install -U <PROJECT>


Uninstall
----------

.. tabbed:: pip

   .. code-block:: sh
      :caption: uninstall

      pip uninstall <PROJECT>


.. tabbed:: module import

   .. code-block:: sh
      :caption: if ``command not found: pip``

      python3 -m pip uninstall <PROJECT>




`pspman <https://<GITHOST>.com/<UNAME>/pspman>`__
=====================================================

(Linux only)

For automated management: updates, etc


Install
--------

.. code-block:: sh

   pspman -s -i https://<GITHOST>.com/<UNAME>/<PROJECT>.git



Update
-------

.. code-block:: sh

    pspman


*That's all.*


Uninstall
----------

Remove installation:

.. code-block:: sh

    pspman -s -d <PROJECT>
