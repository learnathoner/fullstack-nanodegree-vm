-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE Players (
  id SERIAL,
  name TEXT,
  wins INTEGER DEFAULT 0,
  matches INTEGER DEFAULT 0,
  points INTEGER DEFAULT 0,
  PRIMARY KEY (id)
);

CREATE TABLE Matches (
  player1_id INTEGER,
  player1_name TEXT,
  player2_id INTEGER,
  player2_name TEXT,
  p1outcome TEXT,
  matchid SERIAL,
  PRIMARY KEY (matchid),
  FOREIGN KEY (player1_id) REFERENCES players(id),
  FOREIGN KEY (player2_id) REFERENCES players(id)
);

CREATE VIEW v_standings AS
  SELECT id, name, wins, matches FROM Players
  ORDER BY points DESC, name ASC;
