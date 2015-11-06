-- Test suit 8 players tournament

-- Restart ID in players table to correctly record matches

ALTER SEQUENCE players_id_seq RESTART WITH 1;

-- Insert some players

INSERT INTO players(name) VALUES('P1');
INSERT INTO players(name) VALUES('P2');
INSERT INTO players(name) VALUES('P3');
INSERT INTO players(name) VALUES('P4');
INSERT INTO players(name) VALUES('P5');
INSERT INTO players(name) VALUES('P6');
INSERT INTO players(name) VALUES('P7');
INSERT INTO players(name) VALUES('P8');

-- Add some match history

-- R1

INSERT INTO matches(winner, loser) VALUES(1,2);
INSERT INTO matches(winner, loser) VALUES(3,4);
INSERT INTO matches(winner, loser) VALUES(5,6);
INSERT INTO matches(winner, loser) VALUES(7,8);

-- R2

INSERT INTO matches(winner, loser) VALUES(1,3);
INSERT INTO matches(winner, loser) VALUES(5,7);
INSERT INTO matches(winner, loser) VALUES(2,4);
INSERT INTO matches(winner, loser) VALUES(6,8);

-- R3

INSERT INTO matches(winner, loser) VALUES(1,5);
INSERT INTO matches(winner, loser) VALUES(3,2);
INSERT INTO matches(winner, loser) VALUES(7,6);
INSERT INTO matches(winner, loser) VALUES(4,8);

