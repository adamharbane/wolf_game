-- Trigger 1 : Quand un tour est terminé → COMPLETE_TOUR
CREATE OR REPLACE FUNCTION trig_complete_tour()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  -- Si end_time vient d'être modifié (différent de OLD)
  IF NEW.end_time IS NOT NULL AND (OLD.end_time IS NULL OR NEW.end_time <> OLD.end_time) THEN
    CALL COMPLETE_TOUR(NEW.id_turn, NEW.id_party);
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_complete_tour
AFTER UPDATE OF end_time ON turns
FOR EACH ROW
EXECUTE FUNCTION trig_complete_tour();

------------------------------------------------------------

-- Trigger 2 : Quand un joueur est ajouté → USERNAME_TO_LOWER
CREATE OR REPLACE FUNCTION trig_username_lower()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  CALL USERNAME_TO_LOWER();
  RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_username_lower
AFTER INSERT ON players
FOR EACH ROW
EXECUTE FUNCTION trig_username_lower();

