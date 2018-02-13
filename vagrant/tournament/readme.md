# Guide to Tournament database
Program is made to track matches for a Swiss tournament. The SQL file
creates databases and tables to store the information, while the Python
file has functions to use those databases for running tournaments.

## How to use:
  1. From PSQL \i tournament.sql to create database, tables, and to connect
  2. Register players for tournament using registerPlayer(). Count to insure
  an even number of players
  3. Create pairings using the swissPairings() function
  4. Report results of matches using reportMatch(winner,loser)
  5. Continue until winner found for the tournament
  6. To play again, run deleteMatches or deletePlayers and restart  


## Files and description of file contents:
1. **tournament.sql** - Creates the database holding players and match
information
  1. Drops database if exists, creates new tournament database
  2. Connects to database
  3. **Players** TABLE to hold names and id of players
  4. **Matches** TABLE to hold match information (winner, loser)
  5. **v_standing** VIEW returns id, name, wins, matches of player sorted by
  wins
2. **tournament.py** - Python functions using the information in the database
  1. Imports PostgreSQL
  2. **connect()** - Connects to tournament db, returns db and cursor
  3. **deleteMatches()** - Clears Matches table
  4. **deletePlayers()** - Clears Players and Matches tables
  5. **countPlayers()** - Returns count of registered players
  6. **registerPlayer(name)** - Takes name of player and registers them
  7. **playerStandings()** - Returns list of players id,name,wins, and matches
  sorted by win records
  8. **reportMatch(winner,loser)** - Reports the outcome of a match using
  winner and loser ids
  9. **swissPairings()** - Returns list of pairings for next round, in tuples
  of player1id, player1name, player2id, player2name

