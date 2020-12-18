# Job Report

An easy way to see hirring trends for any publicly listed company.


* Free software: MIT license
* Documentation: https://job-report.readthedocs.io.


Installation
--------

```
git clone https://github.com/rjdoubleu/JobReport.git
pip install ./JobReport
```


Requirements
--------
Must add a copy of chromedriver to the JobReport/drivers/ directory

Usage
--------
### CLI
```
cd JobReport
python Jobreport/JobReport.py
```
### Python
```
from JobReport import JobReport
jr = JobReport()
jr.getHoldingsJobCounts()
```

### Docker (coming soon...)
```
cd JobReport/dockerfiles/
docker build -t jobreport:latest .
docker run jobreport:latest
```

### Docker-compose (coming soon...)
```
cd JobReport/dockerfiles/
docker-compose up jobreport
```

Tests (coming soon...)
-------
### Docker (coming soon...)
```
cd JobReport/dockerfiles/
docker build -f Dockerfile.tests -t tests:latest .
docker run tests:latest
```

### Docker-compose (coming soon...)
```
cd JobReport/dockerfiles/
docker-compose up tests
```

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
