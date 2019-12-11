# eduTEAMS Account Registry
[![Build Status](https://travis-ci.org/SURFscz/eduteam-account-registry.svg?branch=master)](https://travis-ci.org/SURFscz/eduteam-account-registry)
[![codecov](https://codecov.io/gh/oharsta/eduteam-account-registry/branch/master/graph/badge.svg)](https://codecov.io/gh/oharsta/eduteam-account-registry)

### [Overview Requirements](#system-requirements)

- Python 3.6.x
- MySQL v8.x
- Yarn 1.x
- node

### [Getting started](#getting-started)

#### [Server](#server)
Create a virtual environment and install the required python packages:
```sh
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
GRANT ALL PRIVILEGES ON ear.* TO 'ear'@'localhost' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON ear_test.* TO 'ear'@'localhost' WITH GRANT OPTION;
```
Ensure MySQL is running and run the Python server with the correct local environment setting:
```sh
PROFILE=local CONFIG=config/test_config.yml python -m server
```
With TESTING=1 no mails will be send. If you do want to validate the mails you can run a fake smtp server with:
```sh
python -m smtpd -n -c DebuggingServer localhost:1025
```
If you want the emails to be opened in the browser when developing add the `OPEN_MAIL_IN_BROWSER=1` to your environment

#### [Client](#client)
First install all dependencies with:
```sh
cd client
yarn install
```
The GUI can be started with:
```sh
cd client
yarn start
```
To create a GUI production build:
```sh
yarn build
```
To analyze the bundle:
```sh
yarn analyze
```
Point your browser to http://localhost:5000/api/users/login?redirect_url=http://www.example.com

### [Testing](#testing)

To run all Python tests and validate syntax / formatting:
```sh
source .venv/bin/activate
pytest server/test
flake8 ./server/
```
To generate coverage reports:
```sh
pytest --cov=server --cov-report html:htmlcov server/test
open htmlcov/index.html
```
To run all JavaScript tests:
```sh
cd client
yarn test
```
Or to run all the tests and do not watch - like CI:
```sh
cd client
CI=true yarn test
```
With the environment variable `CONFIG=config/test_config.yml` the test database is used. After you ran one or all of the
tests the database is left with the test data seed.

###[Deployment](#deployment)

To run AUR in production, we suggest using an Apache server; a single configuration can be used to both serve the static
client scripts, and serve the API (server) via wsgi.  Similar setups are probably possible using nginx etc.

In the explaination below, we assume you are deploying to a server on http://uar.example.org/

 1. Create a client production build as explained above.
 2. Create a Python virtualenv as explained above,
 3. Set up your config file `server/config/config.yml`.  You can base it on the `test_config.yml` file in the same
    directory, but please change at least the following:
    ```yaml
    base_url: http://uar.example.org/
    login_url: http://uar.example.org/api/user/login
    ```
 4. Create a log dir in which the wsgi server user (configurable in the WSGI config below, but `www-data` by default on
	Debian/Ubuntu) can write:
    ```sh
    install -d -m1775 -g www-data log
    ```
 5. Copy the wsgi template `examples/uar-api.wsgi.template` to `./uar-api.wgi` and edit the `source_dir` variable to
    match your setup.
 6. Install Python (version 3) WSGI support for Apache.  In Debian or Ubuntu, this is achieved by installing the package
    `libapache2-mod-wsgi-py3`.
 7. Copy the Apache config template to your Apache config directory (`/etc/apache2/sites-enabled` on Debian/Ubuntu) and
    adjust it to your setup.  At the very least, replace `/YOUR/VENV/DIR` by the directory of the Virtualenv you created
    at step 2, and replace `/YOUR/SOURCE/DIR` by the directory in which you have checked our this repository.
 8. Restart Apache.
 9. Open `http://uar.example.org/api/users/login?redirect_url=http://returnurl.example.com` in your browser to start the
    registration process.




