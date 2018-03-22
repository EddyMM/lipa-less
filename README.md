# PAYG

An online pay as you go POS system

## Getting started
The following instructions detail how to run the app

## Prerequisites
You will need to install the Python libraries used by the app.
You can use `pip` to handle installation of dependencies.
I recommend using a virtual environment(`virtualenv`) to install
these libraries.
```
pip install -r requirements.txt
```

The app uses postgresql so install it using

```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

Furthermore, the app requires you to specify the path to the database. So you'll need to create a user and 
database for the app (any user and database name)
will work. The idea is just to have an accessible database for the app to use.
This link might help in directing on how to do this
[create user and database in psql](https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e)

When you have created the user(name and password) and database, export
this details using this format

`export <APP_NAME>_DATABASE_URL="postgresql+psycopg2://<username>:<password>@<host>/<database>"`

For example

`export LipaLess_DATABASE_URL="postgresql+psycopg2://lipaless_admin:lipaless_pw@localhost/lipaless_db"`


The app also needs a secret key to be used to encrypt passwords

To generate a secret key, use Python os.urandom e.g.

```
$ python
# Python CLI
$ import os
$  os.urandom(24)
``` 

Copy the output.

export the secret key using

`export <APP_NAME>_SECRET_KEY="<output>"`

## Running the app

From the root directory of the project, run
```
cd path_to_project/

python run.py
```

Open a browser (Chrome is good) and type in the URL
displayed in the terminal after running the above command
e.g.
```
    http://127.0.0.1:5000
```

## Built with
- Python Flask (Web Application Framework)

## Authors
- Eddy Mwenda (mwendaeddy@gmail.com)
- Geoffrey Ndungu (jeffkim207@gmail.com)
- Catherine Nyambura (cnyambura043@gmail.com)

## License
...
