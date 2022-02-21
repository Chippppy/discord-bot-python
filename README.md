# Discord-Bot: Project Winston
This bot aims to be a personal discord bot for my friends to use in their servers. 
The bot runs simple commands that looks out for certain messages within the server and completes tasks/returns messages based on the command.
The code uses the MySQL-Connector-Python module as well as the Discord.py module to work.
The bot currently runs on a Raspberry Pi V3 with Raspbian OS.
The database used is a MariaDB, MySQL running on the Pi within a local network environment.

# Help:
## Commands 
These are the commands currently available
### ;help
This command will be responded too by 'Winston' with a list of all the commands available and what they do.
### ;pokemon
This command gives the message author a new random Pokemon and ads it to their personal collection.
### ;inv
This command returns a list of all Pokemon the message author has previously caught.
*This command currently has some bugs, but is still useable*

# Requirements
1. Python and it's following modules installed;
* Discord.py
* dotenv-python
* mysql-connector-python

2. A MySQL database with required tables.
*Information about database will not be given for security reasons*

3. A .env file with the personal variables that will allow you to make the bot personal to your situation.
