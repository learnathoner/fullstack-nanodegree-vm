#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database. Returns DB and cursor"""
    try:
        DB = psycopg2.connect("dbname=tournament")
        cursor = DB.cursor()
        return DB, cursor
    except:
        print("Cannot connect to DB")


def deleteMatches():
    """Remove all the match records from the database. Truncates Matches"""
    DB, cursor = connect()
    delete_query = "TRUNCATE Matches;"
    cursor.execute(delete_query)
    DB.commit()
    DB.close()
    return None


def deletePlayers():
    """Remove all the player records from the database.
    Truncates Players, and Matches due to dependency on Players
    """
    DB, cursor = connect()
    delete_query = "TRUNCATE Players CASCADE;"
    cursor.execute(delete_query)
    DB.commit()
    DB.close()
    return None


def countPlayers():
    """Returns the number of players currently registered."""
    DB, cursor = connect()
    count_query = "SELECT count(*) AS num FROM Players;"
    cursor.execute(count_query)
    player_count = cursor.fetchone()
    DB.close()
    return player_count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
    Once added, assigns a serial ID to each player.
    """
    DB, cursor = connect()
    register_query = "INSERT INTO Players (name) VALUES (%s);"
    # replacing value with tuple to prevent sql injection
    cursor.execute(register_query, (name,))
    DB.commit()
    DB.close()
    return None


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    List of Tuples containing (id, name, wins, matches) sorted by wins,
    Created using the view v_standings
    """
    DB, cursor = connect()
    standing_query = "SELECT * FROM v_standings;"
    cursor.execute(standing_query)
    standings = cursor.fetchall()
    DB.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Inserts record of winner_id and loser_id into Matches
    """
    DB, cursor = connect()
    report_query = "INSERT INTO Matches VALUES (%s, %s);"
    cursor.execute(report_query, (winner, loser))
    DB.commit()
    DB.close()
    return None


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Goes through Standings in pairs, creates tuples containing
    player1id, player1name, player2id, player2name and adds those to list.
    """
    standings = playerStandings()
    matches = []
    for player1, player2 in zip(*[iter(standings)]*2):
        matches.append((player1[0], player1[1], player2[0], player2[1]))
    return matches
