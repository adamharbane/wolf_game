-- Procédure 1 : SEED_DATA
CREATE OR REPLACE PROCEDURE SEED_DATA(nb_players INT, party_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
  i INT := 1;
BEGIN
  WHILE i <= nb_players LOOP
    INSERT INTO turns (id_party, start_time, end_time)
    VALUES (party_id, now(), now() + interval '5 minutes');
    i := i + 1;
  END LOOP;
END;
$$;

-- Procédure 2 : COMPLETE_TOUR
CREATE OR REPLACE PROCEDURE COMPLETE_TOUR(tour_id INT, party_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
  rec RECORD;
  target_counts RECORD;
BEGIN
  -- 1. détecter les positions visées
  FOR target_counts IN
    SELECT target_position_row, target_position_col, COUNT(*) as cnt
    FROM players_play
    WHERE id_turn = tour_id
    GROUP BY target_position_row, target_position_col
  LOOP
    IF target_counts.cnt = 1 THEN
      -- déplacement autorisé (pas de conflit)
      UPDATE players_play
      SET origin_position_row = target_position_row,
          origin_position_col = target_position_col
      WHERE id_turn = tour_id
        AND target_position_row = target_counts.target_position_row
        AND target_position_col = target_counts.target_position_col;
    ELSE
      -- conflit : on ignore tous les déplacements vers cette case
      RAISE NOTICE 'Conflit détecté en (% %), aucun déplacement effectué', 
        target_counts.target_position_row, target_counts.target_position_col;
    END IF;
  END LOOP;
END;
$$;

-- Procédure 3 : USERNAME_TO_LOWER
CREATE OR REPLACE PROCEDURE USERNAME_TO_LOWER()
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE players
  SET pseudo = LOWER(pseudo);
END;
$$;
