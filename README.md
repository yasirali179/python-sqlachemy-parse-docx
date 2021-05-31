# Word DOC parsing
This script gets the files from azure cloud and parse the relevant data 
and store it into database.

## Set up Project
####1. Install libreoffice

For intel base processors: 

    brew install --cask libreoffice

For Apple M1 chip:

    arch -arm64 brew install --cask libreoffice

####2. Create virtual environment with python 3.6

    virtualenv -p /usr/local/lib/python3 venv


####3. Activate virtual environment 
    source venv/bin/activate

####4. Install packages
    pip install -r requirements.txt

##Set up Database
####1. Add database path in db.py
    db_path = <your db path>

####2. Run migration create database
    python db.py
    
##Set up azure cloud storage

####1. Add azure Connection String in main.py
    connection_string = <your azure connection string>
####2. Add container name in main.py
    container_name = <your azure container name>

##Run the script

####1. run main.py file
    python main.py

##Result
You can see results in the database
    
