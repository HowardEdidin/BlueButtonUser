"""
Django settings for bluebuttonuser project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# ConfigParser in Python2 changes to configparser in Python3
# print changes to print() in Python3

from configparser import RawConfigParser

PARSE_INI = RawConfigParser()
# http://stackoverflow.com/questions/4909958/django-local-settings/14545196#14545196


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ast
# import sys
from platform import python_version
from .utils import str2bool, str2int

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

APPLICATION_ROOT = BASE_DIR

# Config file should be installed in parent directory
# format is:
# [global]
# domain = dev.bbonfhir.com
# debug = True
# template_debug = True
# debug_settings = True
# email_host = box905.bluehost.com
#

CONFIG_FILE = 'local.ini'
# Read the config file
PARSE_INI.read_file(open(os.path.join(APPLICATION_ROOT, CONFIG_FILE)))
# Then use PARSE_INI.get(SECTION, VARIABLE) to read in value
# Value is in string format
# Use util functions to convert strings to boolean or Integer


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
# The real value is set in the local_settings.py
# local_settings.py is excluded from the git repository
# Place other important keys, passwords etc. in local_settings.py
# which is called at the end of settings.py

# I recommend setting a default/false value in settings.py
# and then overwriting in local_settings. This keeps the app
# functional if anyone clones the repository
# You can generate a new SECRET_KEY using tools such as
# http://www.miniwebtool.com/django-secret-key-generator/
#

SECRET_KEY = 'FAKE_VALUE_REAL_VALUE_SET_FROM_..LOCAL.INI'
SECRET_KEY = PARSE_INI.get('global', 'secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str2bool(PARSE_INI.get('global', 'debug'))

# TEMPLATE_DEBUG = str2bool(PARSE_INI.get('global', 'template_debug'))
# deprecated in Django 1.8 - Moves to 'DEBUG': in template DICT below

DEBUG_SETTINGS = str2bool(PARSE_INI.get('global', 'debug_settings'))

ALLOWED_HOSTS = []
ADMINS = (
    ('Mark Scrimshire', 'mark@ekivemark.com'),
)

MANAGERS = ADMINS

APPLICATION_TITLE = PARSE_INI.get('global', 'application_title')
if APPLICATION_TITLE == "":
    APPLICATION_TITLE = "BB+ Developer Accounts"

if DEBUG_SETTINGS:
    print("Application: ", APPLICATION_TITLE)
    print("Running on Python_version: ", python_version())
    print("")
    print("BASE_DIR:", BASE_DIR)
    print("APPLICATION_ROOT:", APPLICATION_ROOT)
    FULL_CONFIG_FILE = APPLICATION_ROOT.strip() + '/' + CONFIG_FILE
    print("Config File: ", FULL_CONFIG_FILE)

# Application definition

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Put strings here, like "/home/html/django_templates" or
            # "C:/www/django/templates".
            # Always use forward slashes, even on Windows.
            # Don't forget to use absolute paths, not relative paths.
            # This should always be the last in the list because it is our default.
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django_settings_export.settings_export',
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'debug': str2bool(PARSE_INI.get('global', 'template_debug')),
        },
    },
]

# TEMPLATE_CONTEXT_PROCESSORS = (
# )


# TEMPLATE_DIRS = (
#     # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.
#
#     # This should always be the last in the list because it is our default.
#     os.path.join(BASE_DIR, 'templates'),
#
#)
# List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = ()

DEFAULT_APPS = (
    # django_admin_bootstrapped Must appear ahead of django.contrib.admin
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # add django.contrib.auth to support django registration
    'django.contrib.auth',
    # add django.contrib.sites to support django registration
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    # Add third party libraries here
    'bootstrap3',
    'bootstrapform',
    # this installs django-registration-redux
    'registration',
    'rest_framework',
    'oauth2',
    'oauth2_provider', #django-oauth2-provider
    'corsheaders', #django-cors-headers
    'django_python3_ldap',
    'debug_toolbar', #djang-debug-toolbar
    'ldap3',
    'requests',

)
###############
# IMPORTANT: If running on Apache you need to
# update /etc/apache2/sites-available/default-ssl.conf
# with WSGIPassAuthorization On.
# Insert before WSGIScriptAlias
###############

LOCAL_APPS = (
    # Add custom apps here
    'accounts',
    'apps.subacc',
    'apps.secretqa',
    )

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = "accounts.User"
USERNAME_FIELD = "username"
# AUTHENTICATION_BACKENDS = ['accounts.backends.EmailAuthBackend',]
AUTHENTICATION_BACKENDS = (
    #'django_python3_ldap.auth.LDAPBackend',
    #'django_auth_ldap.backend.LDAPBackend',
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'bbuser.urls'

# Moved wsgi.py to apache2 sub-directory for better security protection
WSGI_APPLICATION = 'bbuser.apache2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DBPATH = os.path.join(BASE_DIR, 'db/db.db')
if DEBUG_SETTINGS:
    print("DBPATH:", DBPATH)


# Standard sqlite3 settings

DB_PLATFORM = PARSE_INI.get('global', 'db_platform')
if DEBUG_SETTINGS:
    print("DB Platform:", DB_PLATFORM)
    # postgresql_psycopg2
if DB_PLATFORM == "postgresql_psycopg2":
    print("Setting up Database with:", DB_PLATFORM)
    DATABASES = {
        'default' : {
            'ENGINE' : 'django.db.backends.postgresql_psycopg2',
            # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME' : 'bbuser',  # Or path to database file if using sqlite3.
            'USER' : 'bluebadmin',  # Not used with sqlite3.
           'PASSWORD' : 'whisky-Washington9876',  # Not used with sqlite3.
            'HOST' : '172.31.13.249',
            # Set to empty string for localhost. Not used with sqlite3.
            'PORT' : '5432',
            # Set to empty string for default. Not used with sqlite3.
        }
    }
else: #  DB_PLATFORM == "sqlite3":
    if DEBUG_SETTINGS:
        print('Setting up Database', DB_PLATFORM)
    DATABASES = {
        'default' : {
            'ENGINE' : 'django.db.backends.sqlite3',
            # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME' : DBPATH,  # Or path to database file if using sqlite3.
            'USER' : '',  # Not used with sqlite3.
           'PASSWORD' : '',  # Not used with sqlite3.
            'HOST' : '',
            # Set to empty string for localhost. Not used with sqlite3.
            'PORT' : '',
            # Set to empty string for default. Not used with sqlite3.
        }
    }

# Plan on sqlite3 for development environment
# Use Postgresql for Production

# Use SQL platform for user and session management

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Get the Server Domain Name. eg. dev.bbonfhir.com
# ie the server name to address this app
DOMAIN = PARSE_INI.get('global', 'domain')

if DEBUG_SETTINGS:
    print("Check the valid site id in the site table")
# SITE_ID = 4 = prod - dev.bbonfhir.com
# SITE_ID = 5 = local - localhost:8000
SITE_ID = 5
if DEBUG_SETTINGS:
    print("SITE_ID: ", SITE_ID)
    print("DOMAIN:  ", DOMAIN)

SSL = str2bool(PARSE_INI.get('global', 'ssl'))
if SSL:
    URL_PRE = "https://"
else:
    URL_PRE = "http://"

if DEBUG_SETTINGS:
    print("Secured: ", URL_PRE, "Running on: ", DOMAIN)

# TODO: Pre-load sites
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'sitestatic'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATIC_URL = '/static/'

STATIC_ROOT = '/var/www/html/dev.bbonfhir.com/'

SESSION_COOKIE_SECURE = False
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# For Django Registration:
# settings are stored in local.ini in parent directory
ACCOUNT_ACTIVATION_DAYS = str2int(
    PARSE_INI.get('global', 'account_activation_days'))
try:
    ACCOUNT_ACTIVATION_DAYS = int(ACCOUNT_ACTIVATION_DAYS)
except:
    ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window; you may,
                                 # of course, use a different value.

# REGISTRATION_AUTO_LOGIN = False # Automatically log the user in.
REGISTRATION_AUTO_LOGIN = str2bool(PARSE_INI.get('global',
                                                 'registration_auto_login'))

# REGISTRATION_FORM = 'accounts.admin.UserCreationForm'

# Django Registration
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
EMAIL_HOST = PARSE_INI.get('global', 'email_host')
EMAIL_HOST = EMAIL_HOST.strip()
# EMAIL_PORT = 1025 # local
# EMAIL_PORT = 645 # SSL
EMAIL_PORT = str2int(PARSE_INI.get('global', 'email_port'))

EMAIL_HOST_USER = PARSE_INI.get('global', 'email_host_user')
EMAIL_HOST_PASSWORD = PARSE_INI.get('global', 'email_host_password')

EMAIL_HTML = str2bool(PARSE_INI.get('global', 'email_html'))

# EMAIL_USE_TLS = True
# Port 465 = SSL
# Port 587 = TLS
# EMAIL_USE_SSL = True
EMAIL_USE_SSL = str2bool(PARSE_INI.get('global', 'email_use_ssl'))

EMAIL_BACKEND_TYPE = PARSE_INI.get('global', 'email_backend_type')
if EMAIL_BACKEND_TYPE == 'smtp':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Default page for Login process
# Setting this to stage 1 of Login with SMS Code
LOGIN_URL = "/accounts/smscode"

# Default Location to redirect to after successful login
# Overridden by next= parameter
LOGIN_REDIRECT_URL = '/'

# SMS code Time out in Minutes (used for Multi-factor Authentication
SMS_LOGIN_TIMEOUT_MIN = 5

DEFAULT_VALID_UNTIL = int(PARSE_INI.get('global', 'default_valid_until'))
if DEFAULT_VALID_UNTIL < 1:
    DEFAULT_VALID_UNTIL = 365

if DEBUG_SETTINGS:
    print("Default_Valid_Until:", DEFAULT_VALID_UNTIL)

# to use console open terminal and run:
# python -m smtpd -n -c DebuggingServer localhost:1025
# Replacing localhost:1025 with EMAIL_HOST:EMAIL_PORT if different
DEFAULT_FROM_EMAIL = PARSE_INI.get('global',
                                   'default_from_email')

if DEBUG_SETTINGS:
    print("Email via %s: %s" % (EMAIL_BACKEND_TYPE, EMAIL_BACKEND))
    print("Account Activation Days: %s" % ACCOUNT_ACTIVATION_DAYS)
    print("Email Host:Port: %s:%s" % (EMAIL_HOST, EMAIL_PORT))
    print(
        "Credentials: [%s]/[%s]" % (EMAIL_HOST_USER,
                                    EMAIL_HOST_PASSWORD))

# END of DJANGO Registration Settings Section

# CORSHEADERS Configuration
# Set ALLOW_ALL to True for testing only
CORS_ORIGIN_ALLOW_ALL = True

# End of CORSHEADERS Section

# Change to OAuth2 Provider Application Model
# OAUTH2_PROVIDER_APPLICATION_MODEL='accounts.MyApplication'

# Add Bootstrap awareness to Crispy Forms
# CRISPY_TEMPLATE_PACK = "bootstrap3"
# CRISPY_FAIL_SILENTLY = not DEBUG

# Django Debug Toolbar
INTERNAL_IPS = '127.0.0.1'
# SHOW_TOOLBAR_CALLBACK = 'bbonfhiruser.debug'
SHOW_TOOLBAR_CALLBACK = 'debug_toolbar.middleware.show_toolbar'

if DEBUG_SETTINGS:
    print("Django Debug Toolbar")
    print("Internal IPs", INTERNAL_IPS)
    print("Debug:", DEBUG)


# Django 1.6+ implement a new test runner
# Suppress error 1_6.W001 by adding:
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Get Local Settings that you want to keep private.
# Make sure Local_settings.py is excluded from Git
# try:
#     from bluebuttonuser.local_settings import *
# except Exception as e:
#     print("ERROR: local_settings not loaded")
#     pass

# SETTINGS EXPORT for django-settings-export context processor
# Explicitly define settings to Export for use in {{ Template Values }}

# GEt a file name that stores words we will use to create fake accounts
WORD_LIST = PARSE_INI.get('global', 'word_dictionary').strip()
WORD_LIST = BASE_DIR + "/words/" + WORD_LIST

if DEBUG_SETTINGS:
    print("===================================")
    print("Testing for Word List:", WORD_LIST)
    FWL = open(WORD_LIST)
    XLEN = 80
    for y in range(2):
        line = FWL.readline(XLEN)
        print(y, ":", line[:-1])
    print("=============================")

DEFAULT_VALID_DAYS = 365

# DONE: Define DEVICE_ACCESS_LOG_DAYS (365)_
# Days to retain Device Access Log entries for a subacc
DEVICE_ACCESS_LOG_DAYS = int(PARSE_INI.get('global',
                                           'device_access_log_days'))
# DEVICE_ACCESS_LOG_DAYS = 365

# number of Device Permission Attempts before flagging Device
# USED and NOT_PERMITTED
DEVICE_PERMISSION_COUNT = int(PARSE_INI.get('global',
                                            'device_permission_count'))
# DEVICE_PERMISSION_COUNT = 3

SECURITY_QUESTION_CHOICES = (
    ('1', 'What is the name of your best friend?'),
    ('2', 'What is the name of your first pet?'),
    ('3', 'What was the color of your favorite car?'),
    ('4', 'How did you go to the prom with?'),
    ('5', 'What is the name of your favorite vacation spot?'),
    ('6', 'What is your favorite magazine?'),
    ('7', 'Who is your favorite Superhero?'),
    ('8', 'Which is your favorite holiday season?'),
    ('9', 'What is your favorite sport?'),
    ('10', 'Who is your favorite sports star?'),
)

SETTINGS_EXPORT = [
    'DEBUG',
    'APPLICATION_TITLE',
    'EMAIL_HOST_USER',
    'SECURITY_QUESTION_CHOICES',
    'DOMAIN',
    'SSL',
    'URL_PRE',
]

if DEBUG_SETTINGS:
    print("SECRET_KEY:%s" % SECRET_KEY)
    print(
        "================================================================")
# SECURITY WARNING: keep the secret key used in production secret!

#######################################
#######################################
# django-auth-ldap

####
# Remote LDAP Check in accounts.views.ldap.validate_ldap_user
# True or False
####

from ldap3 import (Server, Connection,
                   ALL, SUBTREE,
                   LDAPSocketOpenError,
                   LDAPOperationResult,)

REMOTE_LDAP_CHECK = False

AUTH_LDAP_SERVER_URI = "ldap://dev.bbonfhir.com:389"
# LDAP_AUTH_URL = AUTH_LDAP_SERVER_URI
LDAP_AUTH_USE_TLS = False

AUTH_LDAP_BIND_DN = "cn=django-agent,dc=bbonfhir,dc=com"

# Pull from local.ini and remove surrounding double quotes
AUTH_LDAP_SCOPE = PARSE_INI.get('global',
                                'auth_ldap_scope')
AUTH_LDAP_SCOPE = AUTH_LDAP_SCOPE.strip()
AUTH_LDAP_SCOPE = AUTH_LDAP_SCOPE.replace('"', '')
if AUTH_LDAP_SCOPE == "":
    AUTH_LDAP_SCOPE = "ou=people,dc=bbonfhir,dc=com"
LDAP_AUTH_SEARCH_BASE = AUTH_LDAP_SCOPE
LDAP_AUTH_OBJECT_CLASS = "inetOrgPerson"
LDAP_AUTH_CONNECTION_USERNAME = None
LDAP_AUTH_CONNECTION_PASSWORD = None
LDAP_AUTH_USER_FIELDS = {
    "username": "uid",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}
# LDAP_AUTH_USER_LOOKUP_FIELDS = ("cn")
LDAP_AUTH_GET_FIELDS = ["cn", "uid", "givenName",
                        "sn", "mail"]


# BeautifulSoup
BS_PARSER = 'lxml'

FHIR_SERVER = PARSE_INI.get('global', 'fhir_server')
if FHIR_SERVER == '':
    FHIR_SERVER = 'http://fhir.bbonfhir.com/fhir-p'
    # FHIR_SERVER = 'http://localhost:8080/fhir-p'

if DB_PLATFORM == 'sqlite3':
    MEDIA_ROOT = "/Users/mark/Downloads/"
    NPI_SOURCE_FOLDER =  "NPPES_Data_Dissemination_August_2015.zip/"\
                            "NPPES_Data_Dissemination_August_2015/"
    NPI_SOURCE_FILE = "npidata_20050523-20150809-utf8.csv"
else:
    MEDIA_ROOT = "/data/pyapps/media/"
    NPI_SOURCE_FOLDER = "npi/work/"
    NPI_SOURCE_FILE = "npidata_source.csv"


if DEBUG_SETTINGS:
    print("FHIR_SERVER:", FHIR_SERVER)
    print("AUTH_LDAP_SERVER_URI:", AUTH_LDAP_SERVER_URI)
    print("AUTH_LDAP_SCOPE:", AUTH_LDAP_SCOPE)
    print("REMOTE_LDAP_CHECK:", REMOTE_LDAP_CHECK)

    if REMOTE_LDAP_CHECK:
        SRVR = Server(AUTH_LDAP_SERVER_URI, get_info=ALL)
        try:
            CNCT = Connection(SRVR,
                              auto_bind=True,
                              raise_exceptions=False)
            BOUND = CNCT.bind()
            print("Connect:", CNCT)
        except LDAPSocketOpenError:
            CNCT = {}
            print("Server is not reachable")
            print("Connection Exception:", dir(LDAPOperationResult))
#       if hasattr(e, "response"):
#           print("Response:",e.response[0])

        print("Server_Info:", SRVR.info)

        LDAP_TEST = SRVR
        if CNCT:
            LDAP_RESULT = CNCT.search(search_base=AUTH_LDAP_SCOPE,
                                      search_filter=\
                                          "(objectClass=inetOrgPerson)",
                                      search_scope=SUBTREE,
                                      attributes=LDAP_AUTH_GET_FIELDS)
            print("=========================================")
            print("LDAP Access Test:")
            #   print("Response:",c.response)
            print("Result:", CNCT.result)
            for r in CNCT.response:
                print(r['dn'], r['attributes'])

    print("=========================================")
