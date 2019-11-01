=====
argue
=====

Simple tool to execute commands after rearranging command line arguments

.. code-block::

    usage: argue [-h] [-n] [-s SKIP_POSITIONALS] [--prepend-after-operation]
                 [--prepend-all-positionals PREPEND_ALL_POSITIONALS]
                 [--prepend-all-but-last-positional PREPEND_ALL_BUT_LAST_POSITIONAL]
                 [--prepend-all-but-first-positional PREPEND_ALL_BUT_FIRST_POSITIONAL]
                 (-r | -lf | -fl)
                 argv [argv ...]
    
    positional arguments:
      argv
    
    optional arguments:
      -h, --help            show this help message and exit
      -n, --dry-run
    
    Modification:
      -s SKIP_POSITIONALS, --skip-positionals SKIP_POSITIONALS
      --prepend-after-operation
      --prepend-all-positionals PREPEND_ALL_POSITIONALS
      --prepend-all-but-last-positional PREPEND_ALL_BUT_LAST_POSITIONAL
      --prepend-all-but-first-positional PREPEND_ALL_BUT_FIRST_POSITIONAL
    
    Operation:
      -r, --positional-reversal
      -lf, --positional-last-to-first
      -fl, --positional-first-to-last
    

This was initially developed to move the first argument with the last argument in order to make the following command possible.

.. code-block:: bash

    find . -type f -exec rsync -avPHS --relative {} + destination/
  
But this isn't very valid with GNU Find.

.. code-block:: bash

    find . -type f -exec rsync -avPHS --relative destination/ {} +
  
The above very much is valid.  The arguments are now completely out of order.  This is where argue comes in.

.. code-block:: bash

    find . -type f -exec argue -fl -- rsync -avPHS --relative destination/ {} +
  
When rsync is run (evaluate with dry-run mode first!) the first positional argument should become the last.  Hacky but awesome.

Fun test using find again (Skip 1 positional, reverse positionals, prepend some text to all but to the last positional (after applying operation):

.. code-block::

    find /etc/cron.d -type f -exec argue -n --prepend-after-operation --prepend-all-but-last-positional='user@remotehost:' -s 1 -r -- sudo rsync -avPHS --relative /tmp/remote-cronstuff {} +
    Arguments {'argv': ['rsync',
              '-avPHS',
              '--relative',
              '/tmp/remote-cronstuff',
              '/etc/cron.d/.placeholder',
              '/etc/cron.d/rsnapshot',
              '/etc/cron.d/certbot',
              '/etc/cron.d/popularity-contest',
              '/etc/cron.d/mailman'],
     'dry_run': True,
     'positional_first_to_last': False,
     'positional_last_to_first': False,
     'positional_reversal': True,
     'prepend_after_operation': True,
     'prepend_all_but_first_positional': None,
     'prepend_all_but_last_positional': 'user@remotehost:',
     'prepend_all_positionals': None,
     'skip_positionals': 1}
    Original Argv ['sudo',
     'rsync',
     '-avPHS',
     '--relative',
     '/tmp/remote-cronstuff',
     '/etc/cron.d/.placeholder',
     '/etc/cron.d/rsnapshot',
     '/etc/cron.d/certbot',
     '/etc/cron.d/popularity-contest',
     '/etc/cron.d/mailman']
    Modified Argv ['sudo',
     'rsync',
     '-avPHS',
     '--relative',
     'user@remotehost:/etc/cron.d/mailman',
     'user@remotehost:/etc/cron.d/popularity-contest',
     'user@remotehost:/etc/cron.d/certbot',
     'user@remotehost:/etc/cron.d/rsnapshot',
     'user@remotehost:/etc/cron.d/.placeholder',
     '/tmp/remote-cronstuff']
    
    
Beer/Coffee
-----------
See: https://whardier.github.io/
