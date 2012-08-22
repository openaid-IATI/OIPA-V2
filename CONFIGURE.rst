Dependencies
============

===================== ================ ==================
  Package               Required         Recommended     
===================== ================ ==================
  Django                1.4              1.4             
  Python                2.6              2.7             
  MySQL-python          1.2.3            1.2.3           
  South                 0.7.4            0.7.4           
  django-tastypie       0.9.11           0.9.11          
  lxml                  2.3.4            2.3.4           
===================== ================ ==================

Installation Instructions
=========================

1. Install the required dependencies (see table above). The recommended method is to create a virtualenv with the required packages.
2. Create a MySQL databsse (utf8_unicode encoding)
3. If you haven't already, open bash and::

    git clone git://github.com/openaid-IATI/OIPA-V2.git``
    cd OIPA-V2/iati

4. mkdir -p media/utils/temp_files
5. Insert the following lines into ``iati/local_settings.py`` and configure as necessary. ::

    ADMINS = (
        ('Your name', 'your_name@your_domain.com'),
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '***',
            'USER': '***',
            'PASSWORD': '***',
            'HOST': '',
            'PORT': '',
            },
        }

    SERVER_EMAIL = 'server_admin@your_domain.com'

    SECRET_KEY = '' # Must be set to something unguessable,
    # see https://docs.djangoproject.com/en/dev/ref/settings/#secret-key

6. Run ``python manage.py syncdb`` and follow the instructions to create a superuser.
7. Then run::

    python manage.py schemamigration data --initial
    python manage.py schemamigration utils --initial
    python manage.py migrate --fake
    python manage.py runserver 127.0.0.1:8080

Usage
=====

1. You should know be able to log into the admin interface at http://127.0.0.1:8080/admin/
2. Next you should add an IATIXMLSource. Click on the ``Iatixml sources`` link under ``Utils``. Use the ``Add iatixml source`` button and fill in the necessary information before saving.
3. The source should now appear in the list. Click the parse button to parse it. This may take some time, so be patient. The parsing can also be initiated using a manage.py command.
4. If this is successful the activities should be visible via the api. Run ``curl -X GET http://127.0.0.1:8080/api/v2/activities?format=json`` or visit http://127.0.0.1:8080/api/v2/activities?format=json in a browser.
5. Full api documentation can be found at ``http://127.0.0.1:8080/api/v2/docs/`` 

6. It's easy to setup a cronjob for scheduled parse maintenance, an example::

    0 3 * * * ~/your/path/to/virtual/python ~/your/path/to/project/manage.py parse_schedule

   This will run the ``parse_schedule`` command every night at 3 a.m. server time. ``parse_schedule`` checks for a schedule per IATIXMLSource object and parses it if rules are matched.
