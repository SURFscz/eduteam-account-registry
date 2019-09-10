# eduTEAMS Account Registry
[![Build Status](https://travis-ci.org/oharsta/eduteam-account-registry.svg?branch=master)](https://travis-ci.com/oharsta/eduteam-account-registry)
[![codecov](https://codecov.io/gh/oharsta/eduteam-account-registry/branch/master/graph/badge.svg)](https://codecov.io/gh/oharsta/eduteam-account-registry)

### [Overview Requirements](#system-requirements)

- Python 3.6.x
- MySQL v8.x
- Yarn 1.x
- node

### [Getting started](#getting-started)

#### [Server](#server)
Create a virtual environment and install the required python packages:
```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r ./server/requirements/test.txt
```
Connect to your local mysql database: `mysql -uroot` and create the EAR database and user:

```sql
DROP DATABASE IF EXISTS ear;
CREATE DATABASE ear DEFAULT CHARACTER SET utf8;
DROP DATABASE IF EXISTS ear_test;
CREATE DATABASE ear_test DEFAULT CHARACTER SET utf8;
CREATE USER 'ear'@'localhost' IDENTIFIED BY 'ear';
GRANT ALL PRIVILEGES ON *.* TO 'ear'@'localhost' WITH GRANT OPTION;
```
Ensure MySQL is running and run the Python server with the correct local environment setting:
```
PROFILE=local CONFIG=config/test_config.yml python -m server
```
With TESTING=1 no mails will be send. If you do want to validate the mails you can run a fake smtp server with:
```
python -m smtpd -n -c DebuggingServer localhost:1025
```
If you want the emails to be opened in the browser when developing add the `OPEN_MAIL_IN_BROWSER=1` to your environment

#### [Client](#client)
First install all dependencies with:
```
yarn install
```
The GUI can be started with:
```
cd client
yarn start
```
To create a GUI production build:
```
yarn build
```
To analyze the bundle:
```
yarn analyze
```
Point your browser to http://localhost:5000/api/users/login?redirect_url=http://www.example.com

### [Testing](#testing)

To run all Python tests and validate syntax / formatting:
```
source .venv/bin/activate
pytest server/test
flake8 ./server/
```
To generate coverage reports:
```
pytest --cov=server --cov-report html:htmlcov server/test
open htmlcov/index.html
```
To run all JavaScript tests:
```
cd client
yarn test
```
Or to run all the tests and do not watch - like CI:
```
cd client
CI=true yarn test
```
With the environment variable `CONFIG=config/test_config.yml` the test database is used. After you ran one or all of the tests
the database is left with the test data seed.
