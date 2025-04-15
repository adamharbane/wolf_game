-- Fonction 1 : random_position
CREATE OR REPLACE FUNCTION random_position(party_id INT)
RETURNS TABLE(row_pos INT, col_pos INT)
AS $$
BEGIN
  LOOP
    row_pos := floor(random() * 10)::int;
    col_pos := floor(random() * 10)::int;
    
    IF NOT EXISTS (
        SELECT 1 FROM players_play
        WHERE origin_position_row = row_pos::text AND origin_position_col = col_pos::text
    )
    AND NOT EXISTS (
        SELECT 1 FROM obstacles
        WHERE id_party = party_id AND position_row = row_pos::text AND position_col = col_pos::text
    ) THEN
        RETURN NEXT;
        EXIT;
    END IF;
  END LOOP;
END;
$$ LANGUAGE plpgsql;


-- Fonction 2 : random_role
CREATE OR REPLACE FUNCTION random_role(party_id INT)
RETURNS TEXT
AS $$
DECLARE
  wolves_count INT;
  villagers_count INT;
  max_wolves INT;
  max_villagers INT;
BEGIN
  -- Nombre de loups inscrits
  SELECT COUNT(*) INTO wolves_count
  FROM players_in_parties pip
  JOIN roles r ON r.id_role = pip.id_role
  WHERE pip.id_party = party_id AND r.description_role = 'wolf';

  -- Nombre de villageois inscrits
  SELECT COUNT(*) INTO villagers_count
  FROM players_in_parties pip
  JOIN roles r ON r.id_role = pip.id_role
  WHERE pip.id_party = party_id AND r.description_role = 'villager';

  -- Max loups
  SELECT max_quota::int INTO max_wolves FROM roles_quotas rq
  JOIN roles r ON r.id_role = rq.id_role
  WHERE rq.id_party = party_id AND r.description_role = 'wolf';

  -- Max villageois
  SELECT max_quota::int INTO max_villagers FROM roles_quotas rq
  JOIN roles r ON r.id_role = rq.id_role
  WHERE rq.id_party = party_id AND r.description_role = 'villager';

  IF wolves_count < max_wolves THEN
    RETURN 'wolf';
  ELSIF villagers_count < max_villagers THEN
    RETURN 'villager';
  ELSE
    RETURN CASE WHEN random() < 0.5 THEN 'wolf' ELSE 'villager' END;
  END IF;
END;
$$ LANGUAGE plpgsql;

-- Fonction 3 : get_the_winner
CREATE OR REPLACE FUNCTION get_the_winner(party_id INT)
RETURNS TABLE(
  player_name TEXT,
  role TEXT,
  party_name TEXT,
  player_turns INT,
  total_turns INT,
  avg_decision_time FLOAT
)
AS $$
BEGIN
  RETURN QUERY
  SELECT p.pseudo, r.description_role, pa.title_party, 
         COUNT(pp.id_turn) AS player_turns,
         (SELECT COUNT(*) FROM turns WHERE id_party = party_id) AS total_turns,
         AVG(EXTRACT(EPOCH FROM (pp.end_time - pp.start_time))) AS avg_decision_time
  FROM players p
  JOIN players_in_parties pip ON pip.id_player = p.id_player
  JOIN roles r ON r.id_role = pip.id_role
  JOIN players_play pp ON pp.id_players_in_parties = pip.id_players_in_parties
  JOIN parties pa ON pa.id_party = pip.id_party
  WHERE pa.id_party = party_id
  GROUP BY p.pseudo, r.description_role, pa.title_party
  ORDER BY player_turns DESC, avg_decision_time ASC
  LIMIT 1;
END;
$$ LANGUAGE plpgsql;
