-- Suppression de la vue ALL_PLAYERS si elle existe déjà
IF OBJECT_ID('ALL_PLAYERS', 'V') IS NOT NULL
    DROP VIEW ALL_PLAYERS;
GO

-- Création de la vue ALL_PLAYERS
-- Cette vue permet d'afficher, pour chaque joueur ayant
-- participé à au moins une partie, les informations suivantes :
-- • Nom du joueur 
-- • Nombre de parties jouées 
-- • Nombre de tours joués 
-- • Date et heure de la première participation
-- • Date et heure de la dernière action 
CREATE VIEW ALL_PLAYERS
AS
    SELECT
        p.nom AS "Nom_du_joueur",
        COUNT(DISTINCT p.game_id) AS "Nombre_de_parties",
        COUNT(m.move_id) AS "Nombre_de_tours",
        MIN(p.date_inscription) AS "Premiere_participation",
        MAX(m.date_move) AS "Derniere_action"
    FROM players p
        LEFT JOIN moves m ON p.player_id = m.player_id
    GROUP BY p.nom
    HAVING COUNT(DISTINCT p.game_id) > 0
    ORDER BY 
    COUNT(DISTINCT p.game_id),
    MIN(p.date_inscription),
    MAX(m.date_move),
    p.nom;
GO

-- Suppression de la vue ALL_PLAYERS_ELAPSED_GAME si elle existe déjà
IF OBJECT_ID('ALL_PLAYERS_ELAPSED_GAME', 'V') IS NOT NULL
    DROP VIEW ALL_PLAYERS_ELAPSED_GAME;
GO

-- Création de la vue ALL_PLAYERS_ELAPSED_GAME
-- Cette vue affiche pour chaque joueur (et pour chaque partie) :
-- • Nom du joueur,
-- • Nom de la partie,
-- • Nombre de participants à la partie,
-- • Date et l'heure de la première action du joueur dans la partie,
-- • Date et l'heure de la dernière action du joueur dans la partie,
-- • Nombre de secondes écoulées entre la première et la dernière action.
CREATE VIEW ALL_PLAYERS_ELAPSED_GAME
AS
    SELECT
        p.nom AS "Nom_du_joueur",
        g.nom AS "Nom_de_la_partie",
        (SELECT COUNT(DISTINCT p2.player_id)
        FROM players p2
        WHERE p2.game_id = p.game_id) AS "Nombre_de_participants",
        MIN(m.date_move) AS "Premiere_action",
        MAX(m.date_move) AS "Derniere_action",
        DATEDIFF(SECOND, MIN(m.date_move), MAX(m.date_move)) AS "Secondes_passées"
    FROM players p
        JOIN games g ON p.game_id = g.game_id
        LEFT JOIN moves m ON p.player_id = m.player_id
    GROUP BY p.nom, g.nom, p.game_id
    ORDER BY p.nom, g.nom;
GO

-- Suppression de la vue ALL_PLAYERS_ELAPSED_TOUR si elle existe déjà
IF OBJECT_ID('ALL_PLAYERS_ELAPSED_TOUR', 'V') IS NOT NULL
    DROP VIEW ALL_PLAYERS_ELAPSED_TOUR;
GO

-- Création de la vue ALL_PLAYERS_ELAPSED_TOUR
-- Cette vue affiche pour chaque tour d'un joueur (pour chaque partie) :
-- • Nom du joueur
-- • Nom de la partie
-- • Numéro du tour (stocké dans la colonne 'tour' de la table moves)
-- • Date et l'heure du début du tour : la plus ancienne date d'action (MIN(date_move))
-- • Date et l'heure de la prise de décision : la plus récente date d'action (MAX(date_move))
-- • Nombre de secondes écoulées dans le tour pour le joueur, calculé par DATEDIFF entre les deux dates
CREATE VIEW ALL_PLAYERS_ELAPSED_TOUR
AS
    SELECT
        p.nom AS "Nom_du_joueur",
        g.nom AS "Nom_de_la_partie", -- Veillez à ce que la table games possède une colonne 'nom'
        m.tour AS "Numero_du_tour",
        MIN(m.date_move) AS "Debut_du_tour", -- Date et heure de la première action du tour
        MAX(m.date_move) AS "Decision_du_joueur", -- Date et heure de la dernière action du tour
        DATEDIFF(SECOND, MIN(m.date_move), MAX(m.date_move)) AS "Secondes_passées"
    FROM players p
        JOIN games g ON p.game_id = g.game_id
        LEFT JOIN moves m ON p.player_id = m.player_id
    GROUP BY p.nom, g.nom, m.tour
    ORDER BY p.nom, g.nom, m.tour;
GO

-- Suppression de la vue ALL_PLAYERS_STATS si elle existe déjà
IF OBJECT_ID('ALL_PLAYERS_STATS', 'V') IS NOT NULL
    DROP VIEW ALL_PLAYERS_STATS;
GO

-- Création de la vue ALL_PLAYERS_STATS
-- Cette vue affiche pour chaque joueur :
-- • Nom du joueur
-- • Rôle parmi loup et villageois
-- • Nom de la partie
-- • Nombre de tours joués par le joueur
-- • Nombre total de tours de la partie
-- • Vainqueur dépendant du rôle du joueur
-- • Temps moyen de prise de décision du joueur
CREATE VIEW ALL_PLAYERS_STATS
AS
    SELECT
        p.nom AS "Nom_du_joueur",
        p.role AS "Role",
        g.nom AS "Nom_de_la_partie",
        COUNT(DISTINCT m.tour) AS "Nb_tours_joues",
        (SELECT COUNT(DISTINCT tour)
        FROM moves
        WHERE game_id = p.game_id) AS "Nb_total_tours",
        CASE
            WHEN p.role = 'loup' AND g.winner = 'loup' THEN 'Oui'
            WHEN p.role = 'villageois' AND g.winner = 'villageois' THEN 'Oui'
            ELSE 'Non'
        END AS "Vainqueur",
        AVG(DATEDIFF(SECOND, MIN(m.date_move), MAX(m.date_move))) OVER (PARTITION BY p.player_id, p.game_id) AS "Temps_moyen_decision"
    FROM players p
        JOIN games g ON p.game_id = g.game_id
        LEFT JOIN moves m ON p.player_id = m.player_id
    GROUP BY p.nom, p.role, g.nom, p.game_id, g.winner
    ORDER BY p.nom, g.nom;
GO
