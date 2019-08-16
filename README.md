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

Then run following commands:

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

Register new user or update existing user's token:

```
python dbtester.py [code] # get [code] by running gather_keys_oauth2.py
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

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc


