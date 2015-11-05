-- Udacity
-- Full Stack Web Developer Nanodegree
-- Project 2
-- by Federico Vasen

-- Table definitions for the tournament project.
-- Intended to follow SQL style guide available 
-- at http://www.sqlstyle.guide/


-- Create table for storing player data

CREATE TABLE players (
	id		serial		PRIMARY KEY,
	name	varchar(255)
);

-- Create table for storing matches data
-- players.id is set as FK to avoid inserting matches 
-- with players not registered in the database. 
-- A constraint was added to prevent adding matches against oneself.

CREATE TABLE matches (
	id		serial		PRIMARY KEY,
	winner	int 		REFERENCES players(id),
	loser 	int 		REFERENCES players(id), 
	CONSTRAINT no_self CHECK (winner != loser)
);

-- Creates a view to know the current standing of a player at a given moment

CREATE VIEW standings AS 
	SELECT players.id, players.name, count(matches.winner) as wins, count(matches.winner) + count(matches.loser) as played
	FROM players, matches
	GROUP BY players.id;



