# Fitbit VM Server

Data puller: from fitbit API and Django web server to ICTR database.

## Usage

### For first time user

Environment:

* Python 3
* JHU WIN domain computer
* Sequel Server Management Studio (SSMS)
* [MSSQL ODBC Driver 13](https://www.microsoft.com/en-us/download/details.aspx?id=53339)
* Other python libraries: pyodbc, pymssql, cherrypy, fitbit, pytz, etc.

Run following commands:

```
git clone [.git]
source venv/bin/activate
cd python-fitbit
python gather_keys_oauth2.py
pip install [needed modules]
```
In the following browser popup, login with fitbit credentials and save the value of 'code' as CODE, which will be used below.

CTRL-C to close auth server.
```
pip install -r requirements2.txt
```
Run [starter.py](python-fitbit/starter.py) to register ICTR server.
```
python starter.py
```

Modify the code [dbtester.py](python-fitbit/dbtester.py) and [survey_archiver.py](python-fitbit/survey_archiver.py) with your own credentials to ICTR server.
```
python dbtester.py [CODE]
```
Now the token is saved on [tokens.json](python-fitbit/tokens.json), save {user_id} in your head.
```
python dbtester.py
```

Now the user with active token in [tokens.json](python-fitbit/tokens.json) have been updated. 

Check the ICTR database for changes.

### Prostate cancer data puller

Autorun every active user in [tokens.json](python-fitbit/tokens.json):

```
python dbtester.py
```

Register new user or update existing user's token: (get code by running gather_keys_oauth2.py)

```
python dbtester.py [code]
```

Update a certain user's date in a given period:
```
python dbtester.py get [fitbit_uid] [start date, like 2019-08-01] [end date, like 2019-08-05]
```

### Check-in and survey data puller

Update yesterday's data:

```
python survey_archiver.py
```

Update date from a custom date:

```
pyhton survey_archiver.py [date]
```

## Developer Guide

For modify and test:

### For dbtester

Modify. Save. Run.

### For surver archiver

In case you need to modify the Django web server.

Clone the web server [here](https://github.com/fath0218/Fitbit_Webserver_Django).

Get into the directory and log into heroku with this credential:

* anthonysunghoonkim@gmail.com
* Fitbit123

```
cd Fitbit_Webserver_Django
heroku login
```
Link the heroku app with this git directory:
```
heroku git:remote -a jhprohealth
```
After modification:
```
git add .
git commit -m ""
git push heroku master
git push
```
