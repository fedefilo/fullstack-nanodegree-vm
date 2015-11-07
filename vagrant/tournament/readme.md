Tournament Results
Udacity Full Stack Nanodegree 
Project 2
by Federico Vasen


To set up the tournament database, run the SQL script contained in tournament.sql 
using the PostgreSQL psql command line tool.

This will create an empty database and initialize the tournament table.
This last initialization is needed to run the tests contained in tournament_test.py without problems.

To interact with the database, the functions provided in tournament.py are provided.

First, start by signaling that a new tournament has started using newTournament().

Then, register players using registerPlayer(). Newly registered players are automatically enrolled 
in the current tournament. 

If you want to include a player from a previous tournament in the current one, please enroll
him using registerInTournament function.

playerStandings() returns the standings of the players in the current tournament.
historicalStandings() returns the standings of the players in all the tournaments in the database.

swissPairings() returns the pairings in the Swiss tournament system. If there is already a winner,
pairs are not returned, and the function raises a ValueError informing it.

Have fun!
