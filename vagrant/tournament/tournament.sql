-- Drops database if exists, creates new tournament DB
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- Holds player name and id
CREATE TABLE Players (
  id SERIAL,
  name TEXT,
  PRIMARY KEY (id)
);

-- Holds Match records - winner, loser, matchid
CREATE TABLE Matches (
  winner_id INTEGER,
  loser_id INTEGER,
  matchid SERIAL,
  PRIMARY KEY (matchid),
  FOREIGN KEY (winner_id) REFERENCES Players(id),
  FOREIGN KEY (loser_id) REFERENCES Players(id)
);

/* View created left joining Matches to Players, contains id, name,
wins as subquery counting id in winner column, matches as subquery counting id
in winner or loser columns.

Would appreciate constructive criticism on simplifying/cleaning this query
*/
CREATE VIEW v_standings AS
  SELECT id, name,
    (SELECT count(*)
      FROM Matches
      WHERE winner_id = id
    ) AS wins,
    (SELECT count(*)
      FROM Matches
      WHERE (winner_id = id) OR (loser_id = id)
    ) AS matches
  FROM Players LEFT JOIN Matches
    ON Players.id = Matches.winner_id
  -- Group By only worked when including every column, otherwise raised error
  GROUP BY id, name, wins, matches
  ORDER BY wins DESC, name ASC;
