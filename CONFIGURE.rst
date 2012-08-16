+---------------------+----------------+----------------+
+ Package             | Required       | Recommended    |
+---------------------+----------------+----------------+
| Django              | 1.4            | 1.4            |
| Python              | 2.6            | 2.7            |
| MySQL-python        | 1.2.3          | 1.2.3          |
| South               | 0.7.4          | 0.7.4          |
| django-tastypie     | 0.9.11         | 0.9.11         |
| lxml                | 2.3.4          | 2.3.4          |
+---------------------+----------------+----------------+

1. Create a virtualenv with the required packages
2. Create a MySQL database (utf8_unicode encoding)
3. Open bash, cd ~/yourprojectdir/iati
4. configure, paste your settings and save:

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

5. python manage.py syncdb
6. python manage.py schemamigration data --initial
7. python manage.py schemamigration utils --initial
8. python manage.py migrate --fake
9. python manage.py runserver 127.0.0.1 --8080
10. visit http://127.0.0.1:8080/admin/ and add an IATIXMLSource object and use the parse button or a manage command.
12. curl -X GET http://127.0.0.1:8080/api/v2/activities?format=json or visit http://127.0.0.1:8080/api/v2/activities?format=json in a browser

It's easy to setup a cronjob for scheduled parse maintenance, an example:

0 3 * * * ~/your/path/to/virtual/python ~/your/path/to/project/manage.py parse_schedule

This will run the 'parse_schedule' command every night at 3 a.m. server time. parse_schedule checks for a schedule per IATIXMLSource object and parses it if rules are matched.