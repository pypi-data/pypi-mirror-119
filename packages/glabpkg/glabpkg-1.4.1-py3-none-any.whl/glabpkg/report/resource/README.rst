.. {# pkglts, glabreport, after doc
develop: |dvlp_build|_ |dvlp_coverage|_

.. |dvlp_build| image:: {{ gitlab.url }}/badges/develop/pipeline.svg
.. _dvlp_build: {{ gitlab.url }}/commits/develop

.. |dvlp_coverage| image:: {{ gitlab.url }}/badges/develop/coverage.svg
.. _dvlp_coverage: {{ gitlab.url }}/commits/develop


master: |master_build|_ |master_coverage|_

.. |master_build| image:: {{ gitlab.url }}/badges/master/pipeline.svg
.. _master_build: {{ gitlab.url }}/commits/master

.. |master_coverage| image:: {{ gitlab.url }}/badges/master/coverage.svg
.. _master_coverage: {{ gitlab.url }}/commits/master
.. #}

Instructions
------------

To compile the documentation, you need a python environment with sphinx.

.. code-block:: bash

    $ conda activate myenv
    (myenv)$ cd report
    (myenv)$ make html

The resulting document should be in **report/build/html/index.html**

If you want to replay the analysis, all the scripts that generated the figures
are in the **script** folder.
