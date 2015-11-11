# Udacity
# Full Stack Web Developer Nanodegree
# Project 2
# tournament.py -- implementation of a Swiss-system tournament
# by Federico Vasen
# Nov 4, 2015

import psycopg2


def connect():
    """Connect to the PostgreSQL database tournament.  Returns a database connection."""
    try:
        connection = psycopg2.connect("dbname=tournament")
        cursor = connection.cursor()
        return connection, cursor
    except:
        print "Error connecting to database"


def deleteMatches():
    """Remove all the match records from the database."""
    connection, cursor = connect()
    query = "TRUNCATE matches"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection, cursor = connect()
    query = "TRUNCATE enrolled_players, players RESTART IDENTITY CASCADE"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()


def newTournament():
    """Sets the database to record data from a new tournament."""
    connection, cursor = connect()
    query = "INSERT INTO tournament VALUES(nextval('tournament_id_seq'))"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered considering
    all tournaments in the database."""
    connection, cursor = connect()
    query = "SELECT count(*) FROM players"
    cursor.execute(query)
    result = cursor.fetchall()[0][0]
    cursor.close()
    connection.close()
    return result


def registerPlayer(name):
    """Adds a player to the database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    connection, cursor = connect()
    query1 = "INSERT INTO PLAYERS(name) VALUES(%s)"
    param1 = (name, )
    cursor.execute(query1, param1)
    query2 = "INSERT INTO enrolled_players(tournament, player_id) VALUES((SELECT max(id) FROM tournament), (SELECT max(id) FROM players))"
    cursor.execute(query2)
    connection.commit()
    cursor.close()
    connection.close()


def registerInTournament(id_player):
    """Registers player in current tournament.
    Only needed for players that were added for previous tournaments
    and not the current one.

    Args:
      name: the player's id number.
    """
    connection, cursor = connect()
    query = "INSERT INTO enrolled_players(tournament, player_id) VALUES((SELECT max(id) FROM tournament), %s)"
    param = (id_player, )
    cursor.execute(query, param)
    connection.commit()
    cursor.close()
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
    connection, cursor = connect()
    query = "SELECT id_player, name_player, wins, played FROM standings"
    cursor.execute(query)
    standings = cursor.fetchall()
    cursor.close()
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
    connection, cursor = connect()
    query = "SELECT id_player, name_player, wins, played FROM historicalstandings"
    cursor.execute(query)
    standings = cursor.fetchall()
    cursor.close()
    connection.close()
    return standings


def reportMatch(winner, loser):
    """
    Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection, cursor = connect()
    query = "INSERT INTO matches(winner, loser, tournament) VALUES(%s, %s, (SELECT max(id) FROM tournament))"
    param = (winner, loser)
    cursor.execute(query, param)
    connection.commit()
    cursor.close()
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

    # Check if there is a winner
    # (if there is a winner, its win-count is different from the 2nd best)
    if ps[0][2] == ps[1][2]:

        # Create lists to store pairings
        pairs = []

        # Match player with the next player in the table and add the tuple
        # to the list
        for i in range(0, len(ps), 2):
            pairs.append((ps[i][0], ps[i][1], ps[i + 1][0], ps[i + 1][1]))
        # Return the paired matches
        return pairs
    else:
        raise ValueError("There is already a winner!")
