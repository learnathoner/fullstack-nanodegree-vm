#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    delete_query = """
        UPDATE Players
        SET wins = 0, matches = 0, points = 0;
    """
    cursor.execute(delete_query)
    DB.commit()
    DB.close()
    return None


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    #Necessary to delete matches before clearing players, due to foreign key
    delete_query = "DELETE FROM Matches;"
    cursor.execute(delete_query)
    DB.commit()

    delete_query = "DELETE FROM Players;"
    cursor.execute(delete_query)
    DB.commit()
    DB.close()
    return None


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    count_query = "SELECT count(*) AS num FROM Players;"
    cursor.execute(count_query)
    player_count = cursor.fetchall()
    DB.close()

    #for row in player_count:
    #    print row[0]

    return player_count[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    #name = bleach.clean(name)

    DB = connect()
    cursor = DB.cursor()
    register_query = "INSERT INTO Players (name) VALUES (%s);"
    # replacing value with tuple to prevent sql injection
    cursor.execute(register_query, (name,))
    DB.commit()
    DB.close()

    return None

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cursor = DB.cursor()
    standing_query = "SELECT * FROM v_standings;"
    cursor.execute(standing_query)
    standings = cursor.fetchall()
    DB.close()

    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cursor = DB.cursor()

    update_query = """
        UPDATE Players
        SET wins = (wins + %s),
            matches = (matches + 1),
            points = ((wins + %s) / (matches + 1))
        WHERE id = %s;
    """
    cursor.execute(update_query,(1, 1, winner))
    cursor.execute(update_query, (0, 0, loser))

    #Is commit needed after each update query?
    DB.commit()
    DB.close()
    return None



def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()

    DB = connect()
    cursor = DB.cursor()
    delete_query = "DELETE FROM Matches"
    cursor.execute(delete_query)
    DB.commit()

    for player1_info, player2_info in zip(*[iter(standings)]*2):
        play1_id, play1_name = player1_info[0], player1_info[1]
        play2_id, play2_name = player2_info[0], player2_info[1]
        match_query = """
            INSERT INTO Matches (player1_id, player1_name, player2_id, player2_name)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(match_query, (play1_id, play1_name, play2_id, play2_name))
        DB.commit()


    pairings_query = """
        SELECT player1_id, player1_name, player2_id, player2_name
        FROM Matches;
        """
    cursor.execute(pairings_query)
    pairings = cursor.fetchall()

    DB.close()

    return pairings
