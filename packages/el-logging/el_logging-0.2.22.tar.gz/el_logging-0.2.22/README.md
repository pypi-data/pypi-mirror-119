# Easily Launch Logging (el_logging)

* Custom basic logging module
* Loguru based custom logging package for simple python projects.
* Logging to files (all, error, json)
* Custom logging formats
* Custom options as a configs
* Colorful logging
* Multiprocess compatibility (Linux, macOS - 'fork', Windows - 'spawn')

---

## Prerequisites

* **Python (v3.6)**
* **PyPi (v21)**

## Getting started

### 1. Installation

#### A. PyPi install (Recommended)

```sh
## Install or upgrade el-logging package:
pip install --upgrade el-logging

## To uninstall package:
pip uninstall -y el-logging
```

#### B. Manually add to PYTHONPATH (Recommended for development)

```sh
## Clone repository by git
git clone git@bitbucket.org:ellexiinc/elcomm.git

## Install python dependencies
cd el_logging
pip install --upgrade pip
cat requirements.txt | xargs -n 1 -L 1 pip install --no-cache-dir

## Add current path to PYTHONPATH
export PYTHONPATH="$PWD:$PYTHONPATH"
```

#### C. Manually compile and setup (Not recommended)

```sh
## Clone repository by git
git clone git@bitbucket.org:ellexiinc/elcomm.git

## Building python package
cd el_logging
pip install --upgrade pip setuptools wheel
python setup.py build
## Install python dependencies with built package to current python environment
python setup.py install --record installed_files.txt

## To remove only installed el-logging package:
head -n 1 installed_files.txt | xargs rm -vrf
## To remove all installed files and packages:
cat installed_files.txt | xargs rm -vrf
```

### 2. Configuration (You can skip this step, if you don't want to configure)

**IMPORTANT:** First, check **.env.example (environment variables)** file.

Copy **.env.example** file to **.env** and change environment variables:

```sh
cp .env.example .env
vi .env
```

Make **configs** directory inside project's base directory and copy **configs/logger.yaml** file into **configs**.
Then edit variable options:

```sh
mkdir $PROJECT/configs

cp configs/logger.yaml $PROJECT/configs/logger.yaml
vi $PROJECT/configs/logger.yaml
```

### 3. Import module

```python
from el_logging import logger

logger.trace('Tracing...')
logger.debug('Debugging...')
logger.info('Logging info.')
logger.success('Success.')
logger.warning('Warning something.')
logger.error('Error occured.')
logger.critical('CRITICAL ERROR.')


def divide(a, b):
    _result = 0
    try:
        _result = a / b
    except ZeroDivisionError:
        logger.error("'b' argument value is zero!")
        raise
    return _result

try:
    divide(10, 0)
except Exception:
    logger.exception("Failed to divide values:")
```

---

## References

* [https://github.com/Delgan/loguru](https://github.com/Delgan/loguru)
