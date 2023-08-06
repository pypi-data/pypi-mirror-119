Overview
========

.. {# pkglts, glabpkg
{% for badge in doc.badges -%}
{{ badge }}
{% endfor %}

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

{{ doc.description }}
