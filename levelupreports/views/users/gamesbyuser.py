"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from levelupapi.models import Game
from levelupreports.views import Connection
from levelupreports.views import Connection


def usergame_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    g.id,
                    g.name,
                    g.game_type_id,
                    g.min_players,
                    g.max_players,
                    g.difficulty,
                    u.id user_id,
                    u.first_name || ' ' || u.last_name AS full_name
                FROM
                    levelupapi_game g
                JOIN
                    levelupapi_gamer gr ON g.gamer_id = gr.id
                JOIN
                    auth_user u ON gr.user_id = u.id
            """)

            dataset = db_cursor.fetchall()

            # Take the flat data from the database, and build the
            # following data structure for each gamer.
            #
            # {
            #     1: {
            #         "id": 1,
            #         "full_name": "Admina Straytor",
            #         "games": [
            #             {
            #                 "id": 1,
            #                 "title": "Foo",
            #                 "maker": "Bar Games",
            #                 "skill_level": 3,
            #                 "number_of_players": 4,
            #                 "gametype_id": 2
            #             }
            #         ]
            #     }
            # }

            games_by_user = {}

            for row in dataset:
                # Crete a Game instance and set its properties
                game = Game()
                game.name = row["name"]
                game.difficulty = row["difficulty"]
                game.min_players = row["min_players"]
                game.max_players = row["max_players"]
                game.game_type_id = row["game_type_id"]

                # Store the user's id
                uid = row["user_id"]

                # If the user's id is already a key in the dictionary...
                if uid in games_by_user:

                    # Add the current game to the `games` list for it
                    games_by_user[uid]['games'].append(game)

                else:
                    # Otherwise, create the key and dictionary value
                    games_by_user[uid] = {}
                    games_by_user[uid]["id"] = uid
                    games_by_user[uid]["full_name"] = row["full_name"]
                    games_by_user[uid]["games"] = [game]

        # Get only the values from the dictionary and create a list from them
        list_of_users_with_games = games_by_user.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_games.html'
        context = {
            'usergame_list': list_of_users_with_games
        }

        return render(request, template, context)
