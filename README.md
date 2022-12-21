# HitmanCompany
MySQL
You need to install mysql and be running in localhost in order sqlalchemy can connect to the DB

After you have running MySQL

create a cluster called "hitmancompany"
- mysql -uroot -ppassword
- CREATE DATABASE hitmancompany;

Then run the scripts allocated in the folder scripts/ to create the tables and before to run the script 'full_teams.sql' run the python seeder

To install Backend
- cd api
- make install
- make start
  
Once you install everything in the backend you can run the seeder and then the 'full_teams.sql' which populates the table of teams
- source .venv/bin/activate
- python seeder.py

FrontEnd

- cd app/hitman-react
- npm install
- npm start


