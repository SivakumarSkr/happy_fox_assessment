# happy_fox_assessment
This repo contains standalone Python scripts that integrate with the GMail API and perform rule-based operations on emails. 
One script will fetch emails from Gmail and store them in a database, while the other script will process the emails and apply 
specified rules to take appropriate actions.

## Code setup
###Clone the repository
```
https://github.com/SivakumarSkr/happy_fox_assessment.git
```
###Navigate to the project directory:

```
cd happy_fox_assessment
```
###Install packages
```
poetry install
```

##Set up the Postgres database
Ensure that Postgres is installed and running on your system.
###create database
```
create database <database_name>;
```

###create user
```
create user <username> with encrypted password '<password>';
```

###grant permissions
```
grant all privileges on database <database_name> to <username>;
```

###Configure the project environmental variables
Copy the example configuration file and rename it to .env
```
cp .env.example .env
```

Open the .env file and update the database connection details with your Postgres credentials and database information.




