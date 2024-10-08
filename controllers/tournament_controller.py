from views.registration_view import *
from models.tournament import Tournament
import json
import glob
import os


class TournamentController:
    def __init__(self):
        self.tournament = None

    def load_tournament_data(self, name):
        self.tournament = Tournament(name, None, None, None, None)
        is_data_loaded = self.tournament.load_data()
        if not is_data_loaded:
            self.tournament = None

    def create_tournament(self, details = None):
        tmt_name, tmt_location, tmt_start_date, tmt_end_date, tmt_description = (
            create_tournament_view(details)
        )
        if tmt_name == '0' or tmt_location == '0' or tmt_start_date == '0' or tmt_end_date == '0' or tmt_description == '0':
            data = {"option_number":1,
                    "tmt_name":tmt_name,
                    "tmt_location":tmt_location,
                    "tmt_start_date": tmt_start_date,
                    "tmt_end_date": tmt_end_date,
                    "tmt_description": tmt_description
                    }
            with open("resources/resume_file.json","w") as file:
                json.dump(data,file,indent=4)
            return False
        else:
            self.tournament = Tournament(
                tmt_name, tmt_location, tmt_start_date, tmt_end_date, tmt_description
            )
            self.tournament.save_tournament_details()
            return True

    def register_player(self, details= None):
        
        chess_id, last_name, first_name, birthday, country, club_name = (
            register_player_view(details)
        )
        if country == '0' or club_name == '0' or chess_id == '0' or first_name == '0' or last_name == '0' or birthday == '0':
            print("Registration process exited tournament controller part.")
            data = {"option_number":4,
                    "tournament":self.tournament.name,
                    "country":country,
                    "club_name": club_name,
                    "chess_id": chess_id,
                    "last_name": last_name,
                    "first_name": first_name,
                    "birthday":birthday}
            with open("resources/resume_file.json","w") as file:
                json.dump(data,file,indent=4)
            return False
        else:
            print("application closed tournament controller part")
            self.tournament.register_player(
                chess_id, last_name, first_name, birthday, country, club_name
            )
            return True

    def start_tournament(self):
        self.tournament.set_total_nbr_rounds()
        # while True:
        for round in range(self.tournament.number_of_rounds):
            self.tournament.generate_round()
            number_of_winners = self.tournament.start_round()
            if number_of_winners == 1:
                print("final winner decided") 
                break
            print("no final winner yet")
        self.tournament.add_rounds_to_file()

    def see_all_players(self):
        with open("resources/clubs.json", "r") as file:
            data = json.load(file)
            all_players = {}
            for federation in data["federations"]:
                for club in federation["clubs"]:
                    for player in club["players"]:
                        key = f"{player['last_name']} {player['first_name']}"
                        value = f"{player['national_chess_id']}"
                        all_players[key] = value
            all_players = dict(sorted(all_players.items()))

            show_all_players(all_players)

    def see_all_tournaments(self):
        path = os.path.join("resources/tournaments", "*.json")
        file_names = glob.glob(path)
        # print(file_names)
        tournaments = []
        for file_name in file_names:
            with open(file_name) as file:
                data = json.load(file)
                tournaments.append(data)
        show_all_tournaments(tournaments)

    def search_tournament(self):
        print(self.tournament)

    def show_tournament_players(self):
        players = self.tournament.registered_players
        all_players = {}
        # print(players)
        for player in players:
            key = f"{player.last_name} {player.first_name}"
            value = f"{player.national_chess_id}"
            all_players[key] = value
        all_players = dict(sorted(all_players.items()))
        show_all_players(all_players)

    def show_tournament_report(self):
        for round in self.tournament.rounds:
            show_tournament_round(
                round.rnd_name, round.rnd_start_datetime, round.rnd_end_datetime
            )
            for match in round.rnd_matches:
                show_round_matches(match.player1, match.player2)
                
    
        
            
