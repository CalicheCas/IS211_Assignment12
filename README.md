# IS211_Assignment12
Web Development with Flask part two

To run the application follow the steps below:

1. Traverse to the project base path ( IS211_Assignment12)
2. One the CLI run:
    Windows 
    
    C:\IS211_Assignment12> set FLASK_APP=studenttracker.py
    C:\IS211_Assignment12> flask run
    
    Unix
    
    ~/IS211_Assignment12
    $ export FLASK_APP=studenttracker.py
    $ flask run
            
#### Useful tips
Set your FLASK_DEBUG=1 so the flask app can run in debug mode and be able to hot reload instead of having to stop and start the flask app
            
### Database

FLASK_APP is a dependency and must be set to studenttracker.py.

Once flask variable has been set run the following command to
initialize the database.


> flask db init

## Database migrations

> flask db migrate -m "users table"
> flask db upgrade
-m option is optional, it adds a short descriptive text to
the migration
