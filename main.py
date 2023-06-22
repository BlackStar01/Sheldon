
# Constants (Input/Output filenames)
PLAYER_INFO_FILE = 'players_infos.csv'
ROUND_0_FILE = 'round_0.csv'
MATCHES_FILE = 'matches.csv'

# Code here
import csv

class Player:
    def __init__(self, name, game):
        self.name = name
        self.game = game


# Ouvrir et lire les fichiers
with open(PLAYER_INFO_FILE, 'r') as file:
    reader = csv.reader(file)
    players_infos = list(reader)

with open(ROUND_0_FILE, 'r') as file:
    reader = csv.reader(file)
    first_round = list(reader)

#with open(MATCHES_FILE, 'r') as file:
#    reader = csv.reader(file)
#    list_matches = list(reader)


#print(players_infos)
# print(first_round)
# print(first_round[1][0])


# Créez une fonction (ou une classe avec méthodes) qui permet de trouver le coup d'un duel.

def result_duel(player_1, player_2):
    if player_2 is None:
        return player_1

    if player_1.game == player_2.game:
        if player_1.name.lower() < player_2.name.lower():
            print("Same game ... " + player_1.name + " is the winner ")
            return player_1
        else:
            print("Same game ... " + player_2.name + " is the winner ")
            return player_2

    if (player_1.game == "PAPER" and (player_2.game == "ROCK" or player_2.game == "SPOCK")) or (
            player_1.game == "ROCK" and (player_2.game == "LIZARD" or player_2.game == "SCISSORS")) or (
            player_1.game == "SCISSORS" and (player_2.game == "PAPER" or player_2.game == "LIZARD")) or (
            player_1.game == "LIZARD" and (player_2.game == "PAPER" or player_2.game == "SPOCK")) or (
            player_1.game == "SPOCK" and (player_2.game == "ROCK" or player_2.game == "SCISSORS")):
        #print(player_1.name + " is the winner ")
        return player_1
    else:
        #print(player_2.name + " is the winner ")
        return player_2

def display_players(list_players) :
    for player in list_players:
        print(player.name)

# Find player
def find_player_by_round_and_name(player_infos, round, player_name):
    for line in player_infos:
        if line[0] == player_name and line[1] == str(round):
            # print("It's player " + line[0])
            return Player(line[0], line[2])
    return None


current_round = 0
remain_players = []
def single_round_game():
    global remain_players
    remain_players_temporaire = []
    concerned_players = []
    for i in range(0, len(remain_players), 2):
        player_1 = remain_players[i]
        player_2 = remain_players[i + 1] if i + 1 < len(remain_players) else None
        player_1.game = (find_player_by_round_and_name(players_infos, current_round, player_1.name)).game
        player_2.game = (find_player_by_round_and_name(players_infos, current_round, player_2.name)).game
        print(player_1.game)
        print(player_2.game)
        print("--------------------------")
        remain_players_temporaire.append(result_duel(player_1, player_2))
        concerned_players.append(player_1)
        concerned_players.append(player_2)
        with open(MATCHES_FILE, 'a', newline='') as file:
            fieldnames = ['Round', 'Winner', 'Player 1 name', 'Player 1 sign', 'Player 2 name', 'Player 2 sign']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            matches = [
                {'Round': current_round, 'Winner': (result_duel(concerned_players[0], concerned_players[1])).name,
                 'Player 1 name': (concerned_players[0]).name, 'Player 1 sign': (find_player_by_round_and_name(players_infos, current_round, (concerned_players[0]).name)).game,
                 'Player 2 name': (concerned_players[1]).name, 'Player 2 sign': (find_player_by_round_and_name(players_infos, current_round, (concerned_players[1]).name)).game
                 },
            ]
            writer.writerows(matches)
        concerned_players.clear()
    display_players(remain_players)
    remain_players.clear()
    remain_players = remain_players_temporaire.copy()

def many_rounds_game(player_info_list, first_round_list):
    global current_round
    global remain_players
    if current_round == 0:
        concerned_players = []
        for item in first_round_list[1:]:
            if not item:
                continue  # Skip empty elements
            #print(item)
            player_1 = find_player_by_round_and_name(player_info_list, current_round, item[0])
            player_2 = find_player_by_round_and_name(player_info_list, current_round, item[1])
            remain_players.append(result_duel(player_1, player_2))
            concerned_players.append(player_1)
            concerned_players.append(player_2)
            with open(MATCHES_FILE, 'a', newline='') as file:
                fieldnames = ['Round', 'Winner', 'Player 1 name', 'Player 1 sign', 'Player 2 name', 'Player 2 sign']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                matches = [
                    {'Round': current_round, 'Winner': (result_duel(concerned_players[0], concerned_players[1])).name,
                     'Player 1 name': (concerned_players[0]).name, 'Player 1 sign': (concerned_players[0]).game,
                     'Player 2 name': (concerned_players[1]).name, 'Player 2 sign': (concerned_players[1]).game},
                ]
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerows(matches)
                concerned_players.clear()
        #print(" ----------------- ROUND 0 ----------------- ")
        #display_players(remain_players)
    else:
        if len(remain_players) == 1:
            print("TOURNAMENT WINNER : " + remain_players[0].name)
            return
        #print(" ----------------- ROUND " + str(current_round) + " ----------------- ")
        single_round_game()
    current_round += 1
    many_rounds_game([], [])


# player_1 = Player("Alex", "SCISSORS")
# player_2 = Player("Martin", "SCISSORS")
# result_duel(player_1, player_2)

many_rounds_game(players_infos, first_round)


