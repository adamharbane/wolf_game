------------------------------------------------------------
-- Fichier: wv_index.sql
-- Objectif: Appliquer des optimisations et des contraintes
--            sur la base initialement créée avec wv_schema.sql.
--            Ce fichier est exécuté après la création du schéma.
------------------------------------------------------------

-- Création d'un index sur la colonne 'nom' de la table players,
-- afin d'améliorer les requêtes qui filtrent ou trient par le nom du joueur.
CREATE INDEX idx_players_nom ON players(nom);
GO

-- Création d'un index sur la colonne 'date_inscription' de la table players,
-- pour accélérer les requêtes sur la date de la première participation.
CREATE INDEX idx_players_date_inscription ON players(date_inscription);
GO

-- Création d'un index sur la colonne 'game_id' de la table players,
-- utile pour les jointures entre players et games.
CREATE INDEX idx_players_game_id ON players(game_id);
GO

-- Création d'un index sur la colonne 'date_move' de la table moves,
-- afin d'optimiser les requêtes qui recherchent la première ou dernière action.
CREATE INDEX idx_moves_date_move ON moves(date_move);
GO

-- Création d'un index sur la colonne 'player_id' de la table moves,
-- qui facilite les jointures entre moves et players.
CREATE INDEX idx_moves_player_id ON moves(player_id);
GO

------------------------------------------------------------
-- Fin du fichier wv_index.sql
------------------------------------------------------------
