# Udacity
# Full Stack Web Developer Nanodegree
# Project 2
# tournament.py -- implementation of a Swiss-system tournament
# by Federico Vasen
# Nov 4, 2015

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM matches")
    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM enrolled_players")
    cursor.execute("DELETE FROM players")
    connection.commit()
    connection.close()


def newTournament():
    """Sets the database to record data from a new tournament."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO tournament VALUES(nextval('tournament_id_seq'))")
    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered considering
    all tournaments in the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM players")
    result = cursor.fetchall()[0][0]
    connection.close()
    return result


def registerPlayer(name):
    """Adds a player to the database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO PLAYERS(name) VALUES(%s)", (name, ))
    connection.commit()
    cursor.execute(
        "INSERT INTO enrolled_players(tournament, player_id) VALUES((SELECT max(id) FROM tournament), (SELECT max(id) FROM players))")
    connection.commit()
    connection.close()


def registerInTournament(id_player):
    """Registers player in current tournament.
    Only needed for players that were added for previous tournaments
    and not the current one.

    Args:
      name: the player's id number.
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO enrolled_players(tournament, player_id) VALUES((SELECT max(id) FROM tournament), %s)", (id_player, ))
    connection.commit()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records in the current
    tournament, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id_player, name_player, wins, played FROM standings")
    standings = cursor.fetchall()
    connection.close()
    return standings


def historicalStandings():
    """Returns a list of the players and their win records, sorted by wins,
    considering all tournaments.
    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id_player, name_player, wins, played FROM historicalstandings")
    standings = cursor.fetchall()
    connection.close()
    return standings


def reportMatch(winner, loser):
    """
    Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO matches(winner, loser, tournament) VALUES(%s, %s, (SELECT max(id) FROM tournament))", (winner, loser))
    connection.commit()
    connection.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      If there is no winner already returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
      If there is already a winner, throws an error.
    """
    # Get player standings as list of tuples
    ps = playerStandings()

    # Create an empty list to store pairings
    pairs = []

    # Check if there is a winner
    # (if there is a winner, its win-count is different from the 2nd best)
    if ps[0][2] == ps[1][2]:

        # Match player with the next player in the table and add the tuple
        # to the list
        for i in range(0, len(ps), 2):
            pairs.append((ps[i][0], ps[i][1], ps[i + 1][0], ps[i + 1][1]))
        # Return the paired matches
        return pairs
    else:
        raise ValueError("There is already a winner!")
