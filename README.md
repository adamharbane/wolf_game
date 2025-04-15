# Wolf Game

Ce projet est une application de jeu développée en plusieurs modules, incluant un moteur d'administration, un moteur de jeu, des interfaces clients (HTTP et TCP) ainsi que des serveurs. Ce dépôt Git contient également des scripts SQL pour la création et l'optimisation de la base de données.

Prérequis
Docker et Docker Compose installés

Git pour cloner le projet

Commandes Docker Importantes
Utilisez les commandes ci-dessous pour gérer vos conteneurs :

Arrêter et supprimer les conteneurs et les volumes persistants :

```sh
docker-compose down -v
```

Construire et lancer les conteneurs en mode interactif :

```sh
docker-compose up --build
```

Lancer les conteneurs en arrière-plan (mode détaché) :

```sh
docker-compose up -d
```

Afficher la liste de tous les conteneurs (actifs ou non) :

```sh
docker-compose ps -a
```

Afficher les logs du conteneur PostgreSQL (flask_db) :

```sh
docker logs flask_db
```

Accès à la Base de Données (PostgreSQL)
Pour interagir avec PostgreSQL, vous pouvez utiliser plusieurs méthodes :

Utiliser docker exec pour ouvrir une session psql dans le conteneur :

```sh
docker exec -it flask_db psql -U flask_user -d flask_db
```

Utiliser psql directement (si PostgreSQL est exposé sur votre machine) :


```sh
psql -U flask_user -d flask_db
```

Ouvrir un shell interactif dans le conteneur PostgreSQL :

```sh
docker-compose exec db bash
```

Puis, dans ce shell, lancer psql :

```sh
psql -U flask_user -d flask_db
```

Commandes SQL dans psql
Une fois connecté à la base, utilisez :

Liste des tables :

```sh
\dt
```

Liste des vues :

```sh
\dv
```

Quitter psql :

```sh
\q
```

Remarques
Les scripts d'initialisation SQL (par exemple, wv_schema.sql, wv_index.sql et wv_views.sql) sont exécutés automatiquement lors de la première initialisation de la base de données.

Pour tester des modifications dans vos scripts SQL, n'oubliez pas de supprimer les volumes persistants (avec docker-compose down -v) pour forcer leur réexécution.

Ce README vous fournit les commandes essentielles pour démarrer, construire, surveiller vos conteneurs et interagir avec la base de données PostgreSQL. N'hésitez pas à l'enrichir au fur et à mesure que le projet évolue.