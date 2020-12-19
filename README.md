# Job Report

An easy way to see hirring trends for any publicly listed company. Eventually we will want to automatically detect undervalued companies based on their financial report, sector performance, and hirring trends.


* Free software: MIT license
* Documentation: https://job-report.readthedocs.io.


Installation
--------

```
git clone https://github.com/rjdoubleu/JobReport.git
pip install ./JobReport
```

Usage
--------
### CLI
```
cd JobReport
python Jobreport/JobReport.py
```
### Python
```
from JobReport.JobReport import JobReport
jr = JobReport()
jr.getHoldingsJobCounts()
```

### Docker
```
cd JobReport
docker build -t jobreport:latest -f dockerfiles/Dockerfile .
docker run -it jobreport:latest
```

### Docker-compose (coming soon...)
```
cd JobReport
docker-compose up jobreport
```

Tests (coming soon...)
-------
### Docker (coming soon...)
```
cd JobReport
docker build -f dockerfiles/Dockerfile.tests -t tests:latest .
docker run tests:latest
```

### Docker-compose (coming soon...)
```
cd JobReport
docker-compose up tests
```

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
