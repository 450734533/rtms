AutoTest mange system
=====

atms is a Django project to autotest interface.

Quick Start
-----------

1.  Create virtualenv
   Run `pip install virtualenv` to install virtualenv.

   Run `virtualenv ~/envs/atms` to create virtualenv.

   Run `. ~/envs/atms/bin/active` to activate it.

   Run `pip install -r requirements.txt` to install all requirements.

2.  Create database
   Run `CREATE DATABASE atms  DEFAULT CHARSET utf8 COLLATE utf8_general_ci;`.

3.  Make migrations
   Run `python manage.py makemigrations` to make migrations.

   Run `python manage.py migrate` to create the models.

4.  Start the development server
   Run `python manage.py runserver` and visit http://127.0.0.1:8000

Install Google Protobuf (prepare protobuf-2.6.1.tar.gz)
  1).  Install Google Protobuf
    1. # tar xvfz protobuf-2.6.1.tar.gz
    2. # cd protobuf-2.6.1
    3. # ./configure --prefix=/usr/local/protobuf
    4. # make;make check
    5. # make install
    6. # vim ~/.bash_profile
    7. add "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/protobuf/lib
           export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/protobuf/lib/
           export PATH=$PATH:/usr/local/protobuf/bin/"
      below "export PATH"
    8. # source ~/.bash_profile
    9. check whether the Google Protobuf installation is successful
      # protoc --version
  2).  Install protobuf for python
    1. # cd protobuf-2.6.1/python
    2. # python setup.py build
    3. # python setup.py install
    4. chek whether the protobuf for python installation is successful
       # python
       >>> import google.protobuf

#Fix celery bug
http://stackoverflow.com/questions/39664493/using-django-celery-beat-locally-i-get-error-periodictask-object-has-no-attrib
98  Model = type(self.model)
99  obj = Model._default_manager.get(pk=self.model.pk)

Start Celery services

celery worker -A atms --loglevel=INFO -n adms_worker -Q atms_interface_task -c 2
celery beat -A atms --loglevel=INFO