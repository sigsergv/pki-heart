This section is temporary and will be deleted later.

## External docs and APIs

https://bulmatemplates.github.io/bulma-templates/templates/inbox.html
https://github.com/BulmaTemplates/bulma-templates/blob/master/templates/inbox.html
https://github.com/BulmaTemplates/bulma-templates/blob/master/css/inbox.css

## Initial development

Basic models development cycle until initial release:

  1. Modify model (e.g. `pki_heart/camanager/models.py`)
  2. Make migrations: `python manage.py makemigrations`
  3. Renew initial migrations: `python manage.py makemigrations`
  4. Drop all tables and initialize permissions again:
      `DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public to pki_heart_user;`
  6. Initialize database: `python3 manage.py migrate`

Radical approach:

  1. Modify model (e.g. `pki_heart/camanager/models.py`)
  2. Delete existing migrations: `rm -f {camanager,accounts}/migrations/*.py`
  3. Make migrations from scratch: `python3 manage.py makemigrations`
  4. Drop all tables and initialize permissions again:
      `DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public to pki_heart_user;`
  6. Initialize database: `python3 manage.py migrate`

## Create new app

Create new app `accounts`: `python3 manage.py startapp accounts`
