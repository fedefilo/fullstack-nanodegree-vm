-- Udacity
-- Full Stack Web Developer Nanodegree
-- Project 2
-- by Federico Vasen

-- Schema definitions for the tournament project.
-- Intended to follow SQL style guide available 
-- at http://www.sqlstyle.guide/


-- Create database schema

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- Connect to new database

\c tournament


-- Create tournament table

CREATE TABLE tournament (
	id		serial		PRIMARY KEY
);

-- Create table for storing player data

CREATE TABLE players (
	id		serial		PRIMARY KEY,
	name	varchar(255)
);

-- Create table for storing players' enrollment in tournaments

CREATE TABLE enrolled_players (
	tournament 		int 	REFERENCES tournament(id),
	player_id		int 	REFERENCES players(id),
	PRIMARY KEY (tournament, player_id) 
);


-- Create table for storing matches data
-- players.id is set as FK to avoid inserting matches 
-- with players not registered in the database. 
-- A constraint was added to prevent adding matches against oneself.

CREATE TABLE matches (
	winner	int 		REFERENCES players(id),
	loser 	int 		REFERENCES players(id),
	tournament int 		REFERENCES tournament(id),
	PRIMARY KEY (winner, loser, tournament),
	CONSTRAINT no_self CHECK (winner != loser)
);

-- 

-- Creates a view to know the current standing of players at a given moment
-- of the current tournament

CREATE VIEW standings AS 
SELECT players.id as ID_player,
   	   players.name as Name_player, 
 	   (SELECT count(*) 
 	   	  FROM matches 
     	 WHERE (winner = players.id OR loser = players.id) AND matches.tournament = (SELECT max(id) FROM tournament)) AS played,   
 	   (SELECT count(*) 
 	   	  FROM matches 
 	   	 WHERE winner = players.id AND matches.tournament = (SELECT max(id) FROM tournament)) AS wins 
  FROM players 
  WHERE players.id IN 
  		(SELECT player_id 
  		   FROM enrolled_players 
  		  WHERE tournament = (SELECT max(id) FROM tournament))
  ORDER BY wins DESC;

-- Creates a view with the historical standings of all players registered in 
-- the DB 

CREATE VIEW historicalstandings AS 
SELECT players.id as ID_player,
   	   players.name as Name_player, 
 	   (SELECT count(*) 
 	   	  FROM matches 
     	 WHERE winner = players.id OR loser = players.id) AS played,   
 	   (SELECT count(*) 
 	   	  FROM matches 
 	   	 WHERE winner = players.id) AS wins 
  FROM players 
  ORDER BY wins DESC;

-- Initializes tournament table to prevent tournament_test.py from 
-- throwing an error

INSERT INTO tournament VALUES(nextval('tournament_id_seq'))