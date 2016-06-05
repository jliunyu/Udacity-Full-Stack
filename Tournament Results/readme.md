1. The project is "Tournament Result" while include three files, they are tournament.sql, tournament.py and tournament_test.py. The main function of the project is to develop a database schema to store the game matches between players. Then query this data and determine the winners of various games.

2. The file tournament.sql created two tables, players and matches, and also an view called standings. The table player which is used to store players name and id, there are two columns in the table, they are players' id and name. The other table matches stores match id, winner and loser of a game. 

3. The file tournament.py include functions deleteMathces, deletePlayers, countPlayers, registerPlayer and the parameter of it is name, playerStandings, 
reportMatch and the parameters of it are winner and loser, swissPairings

4. The file tournament_test.py is used to tests all the functions in tournament.py

5. The python version 2.7.6 should be installed before running the program, and the database is postgres, version is 9.3.9, the vagrant version is 1.7.4, the virtual box version is 5.0.0.

6. how to run the code: copy tournament.sql, tournament.py and tournament_test.py to vagrant/tournamet. Start up the vagrant using command vagrant up, then SSH into vagrant using command Vagrant SSH.

Using command cd /vagrant/tournament
then run the command psql -f tournament.sql to set up the database
then run the command python tournament_test.py to test the API

7. List of Author: Jane