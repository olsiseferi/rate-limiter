
# Rate Limiter via python

A simple repo implementing 4 rate limiting algorithms using only python, flask and schedule library.

[![System Design](https://img.shields.io/badge/system--design-rate--limiter-brightgreen?style=for-the-badge)]()

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


## Installation

Its a prerequisite that you have python and pip installed.

First clone this repository, after that you need to create a virtual environment using venv, and activate it. (For python3 there's no additional installation required)

```bash
python3 -m venv venv

source venv/bin/activate
```
After that you can install all the required dependencies.

```bash
pip3 install -r requirements.txt
```

Run the specific file
```bash
FLASK_APP={rate_limit_scipt_name}.py flask run

Example:
FLASK_APP=tokenbucket.py flask run
```


    
## Authors

- [@olsiseferi](https://www.linkedin.com/in/olsi-seferi/)


