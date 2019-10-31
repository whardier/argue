=====
argue
=====

Simple tool to execute commands after rearranging command line arguments

.. code-block::

  usage: argue [-h] [-n] (-r | -lf | -fl) argv [argv ...]

  positional arguments:
    argv

  optional arguments:
    -h, --help            show this help message and exit
    -n, --dry-run
    -r, --positional-reversal
    -lf, --positional-last-to-first
    -fl, --positional-first-to-last

This was initially developed to swap the first argument with the last argument in order to make the following command possible.

.. code-block:: bash

  find . -type f -exec rsync -avPHS --relative {} + destination/
  
But this isn't very valid with GNU Find.

.. code-block:: bash

  find . -type f -exec rsync -avPHS --relative destination/ {} +
  
The above very much is valid.  The arguments are now completely out of order.  This is where argue comes in.

.. code-block:: bash

  find . -type f -exec argue -fl -- rsync -avPHS --relative destination/ {} +
  
When rsync is run (evaluate with dry-run mode first!) the first positional argument should become the last.  Hacky but awesome.
