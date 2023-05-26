# happy_fox_assessment
This repo contains standalone Python scripts that integrate with the GMail API and perform rule-based operations on emails. 
One script will fetch emails from Gmail and store them in a database, while the other script will process the emails and apply 
specified rules to take appropriate actions.

## Code setup
### Clone the repository
```
https://github.com/SivakumarSkr/happy_fox_assessment.git
```
### Navigate to the project directory:

```
cd happy_fox_assessment
```
### Install packages
```
poetry install
```

## Set up the Postgres database
Ensure that Postgres is installed and running on your system.
### create database
```
create database <database_name>;
```

### create user
```
create user <username> with encrypted password '<password>';
```

### grant permissions
```
grant all privileges on database <database_name> to <username>;
```

### Configure the project environmental variables
Copy the example configuration file and rename it to .env

```
cp .env.example .env
```

Open the .env file and update the database connection details with your Postgres credentials and database information.

## Set up Gmail API
### Create GCP project and enable the Gmail API:
* Go to the [GCP Console](https://console.cloud.google.com/) and create a new project.

#### Enable the Gmail API:

* Go to the [API Library](https://console.cloud.google.com/apis/library) in your GCP project.

* Search for "Gmail API" and click on it.

* Click the "Enable" button.

### Set up OAuth 2.0 credentials:

* Go to the [Credentials](https://console.cloud.google.com/apis/credentials) page in your GCP project.

* Click on "Create credentials" and select "OAuth client ID".

* Choose "Desktop app" as the application type.

* Download the JSON file containing the credentials.

* Rename the JSON file to `credentials.json` and move it to the project's root directory.

## rules
please refer rules.json.example for learn how write rules

## Usage

### Run email fetching script
```
poetry run python3 email_fetcher.py
```

### Run email processor script
```
poetry run python3 process_email.py
```




