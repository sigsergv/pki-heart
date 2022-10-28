# PKI Heart - PKI/Certificate Lifecycle Management Software

## Development mode

By default it's assuming you are working in project root directory with files `README.md` and `requirements.txt`.

*PKI Heart* is written in python3 and doesn't support python version 2 or python3 version lesser than 3.8.

We use postresql for both development and production so you need to install this database server first. On Linux use your
distribution commands like `apt install postgresql`, on Macos install [Postgres.app](https://postgresapp.com).

*PKI Heart* uses venv for development, so initialize it first and verify:

    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ command -v python3
    /Users/serge/projects/pki-heart/.venv/bin/python3
    $ python3 -m pip --version
    pip 22.2.2 from /Users/serge/projects/pki-heart/.venv/lib/python3.10/site-packages/pip (python 3.10)
    $ python3 -m pip install wheel
    $ python3 -m pip install -r requirements.txt 

If you are using Macos please read section [Macos notes](#macos-notes) how to setup postgres properly.

Create postresql user:

    $ createuser pki_heart_user

Create database:

    $ createdb pki_heart_db

Set user password and privileges:

    $ psql -d postgres
    postgres=# ALTER USER pki_heart_user WITH ENCRYPTED PASSWORD 'pki_heart_pass';
    postgres=# GRANT ALL PRIVILEGES ON DATABASE pki_heart_db to pki_heart_user;
    \q
    $ psql -d pki_heart_db
    pki_heart_db=# GRANT ALL ON SCHEMA public to pki_heart_user;
    \q

Check user access:

    $ psql -U pki_heart_user -d pki_heart_db
    Password for user pki_heart_user:
    psql (15.0)
    Type "help" for help.

    pki_heart_db=>

Set up connection service file `~/.pg_service.conf`:

    [pki_heart]
    host=localhost
    port=5433
    dbname=pki_heart_db
    user=pki_heart_user

Set up password file `pki_heart/.pki_heart_pgpass`:

    localhost:5432:pki_heart_db:pki_heart_user:pki_heart_pass

Initialize database:

    $ cd pki_heart
    $ python3 manage.py migrate

We do not use django admin and superuser so you are don't need to configure them.

Default user login name is `admin` and password is `setup`.

## Macos notes

By default postgresql commands like `createdb` or `psql` are not available inside terminal shell session. You can follow
instructions on site <https://postgresapp.com> to add them permanently or use command below to enable for current shell
session only:

    $ export PATH=/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH

By default Postgres.app allows connections to databases without authentication, if you want to enable security
you must open configuration file `hba.conf` in text editor and explicitly set access up like this:

    # TYPE  DATABASE        USER            ADDRESS                 METHOD

    # "local" is for Unix domain socket connections only
    local   postgres        all                                     trust
    local   all             serge                                   trust
    local   all             all                                     password

    # IPv4 local connections:
    host    postgres        all             127.0.0.1/32            trust
    host    all             all             127.0.0.1/32            password

    # IPv6 local connections:
    host    all             all             ::1/128                 password