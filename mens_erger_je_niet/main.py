#game imports
import random
import html_exporter as html
import save_load as s_v
def num_of_players():
    MAX_PLAYERS = 4
    MIN_PLAYERS = 2
    while True:
        number_players = input("How many poeple wants to play the game [2-4]: ")
        if not number_players.isdigit():
            print("Invalid input")
        elif int(number_players) > MAX_PLAYERS or int(number_players) < MIN_PLAYERS:
            print("Invalid input it must be between 2 and 4 players")
        else:
            number_players = int(number_players)
            break  
    return number_players


def players_info(num_of_players):
    COLORS = ['red','green','black','yellow']
    players_dictionary = {}
    player_num = 0
    while len(players_dictionary) != num_of_players:
        player_color = input(f"Choose a color for player #{player_num + 1} {COLORS}: ").lower()
        if player_color not in COLORS:
            print(f"Invalid input it must be one of these colors: {COLORS}")
        else:
            players_dictionary[player_num] = {}
            players_dictionary[player_num]['color'] = player_color
            players_dictionary[player_num]['starting'] = player_num * 10
            players_dictionary[player_num]['available'] = 4
            players_dictionary[player_num]['home'] = 0
            players_dictionary[player_num]['active'] = []
            player_num += 1
            COLORS.remove(player_color)
    return players_dictionary


def game_representation(players_dictionary):
    BOARD_LENGTH = 40
    print("Player")
    for player in players_dictionary:
        print(f"{player}. {players_dictionary[player]['color']} (starting square: {players_dictionary[player]['starting']},pawns available: {players_dictionary[player]['available']},pawns home: {players_dictionary[player]['home']})")
    print("Board: ")
    for player in players_dictionary:
        for number in range(0,BOARD_LENGTH):
            for pawn in players_dictionary[player]['active']:
                if pawn == number:
                    print(f"{number}: {players_dictionary[player]['color']}")


def roll_dice():
    dice = input("Press enter to roll the dice....")
    if not dice.isdigit():
        dice = random.randint(1, 6)
    else:
        dice = int(dice)
    print(f"You rolled {dice}!")
    return dice



def add_pawn(dice,player_info,players_dictionary):
    if player_info['available'] > 0 and player_info['starting'] not in player_info['active']:
        player_info['available'] -= 1
        new_position = player_info['starting']
        check_collition(new_position, players_dictionary)
        player_info['active'].append(player_info['starting'])
        print("Placing a pawn on the starting square")
    else:
        move_pawn(dice, player_info, players_dictionary)



def move_pawn(dice,player_info,players_dictionary):
    if len(player_info['active']) == 0:
        print("No moveable pawns.")
    elif len(player_info['active']) == 1:
        old_position = player_info['active'][0]
        new_position = check_home(player_info, dice, old_position)
        check_collition(new_position, players_dictionary)
        if isinstance(new_position, int) and not isinstance(new_position, bool):
            player_info['active'][0] = new_position
            print(f"Pawn moving from {old_position} to {new_position}")
    else:
        while True:
            print("The pawn at which square would you like to move? (",end='')
            pawns_list = [str(pawn) for pawn in player_info['active']]
            pawn = ','.join(pawns_list)
            print(pawn,') ',end='')
            pawn_to_move = input("")
            if not pawn_to_move.isdigit():
                print("Invalid input must be a number")
                continue
            elif int(pawn_to_move) not in player_info['active']:
                print("Invalid input number")
                continue
            else:
                pawn_to_move = int(pawn_to_move)
                break
        
        pawn_index = player_info['active'].index(pawn_to_move)
        old_position = player_info['active'][pawn_index]
        new_position = check_home(player_info, dice, old_position)
        check_collition(new_position, players_dictionary)
        if isinstance(new_position, int) and not isinstance(new_position, bool):
            player_info['active'][pawn_index] = new_position
            print(f"Pawn moving from {old_position} to {new_position}")


def check_collition(new_position,players_dictionary):
    for player in players_dictionary:
        if new_position in players_dictionary[player]['active']:
            players_dictionary[player]['active'].remove(new_position)
            players_dictionary[player]['available'] += 1
            print(f"Pawn eliminated on position {new_position}")


def check_home(player_info,dice,old_position):
    BOARD_LENGTH = 40
    new_position = old_position + dice

    if new_position >= BOARD_LENGTH:
        new_position = new_position -BOARD_LENGTH
        if player_info['starting'] == new_position:
            player_info['home'] += 1
            player_info['active'].remove(old_position)
            print("Pawn has arrived home")
            return True
        elif new_position > player_info['starting']:
            print("Pawn would go past home")
            return True
    else:
        if new_position == player_info['starting']:
            player_info['home'] += 1
            player_info['active'].remove(old_position)
            print("Pawn has arrived home")
            return True
        elif old_position < player_info['starting'] and new_position > player_info['starting']:
            print("Pawn would go past home")
            return True
    return new_position

def check_winner(players_dictionary):
    for player in players_dictionary:
        if players_dictionary[player]['home'] >= 4:
            print(f"Player: {players_dictionary[player]['color']} congratulation you have won!!!")
            return True


def main():
    print("Welcome to the killer pawn game!!")
    try:
        with open('game_state.txt','r') as txt_file:
            players_dictionary = s_v.load_game(txt_file)
    except FileNotFoundError:
        players_dictionary = players_info(num_of_players())
    start = True
    while start:
        for player in players_dictionary:
            print()
            s_v.save_game(players_dictionary, player)
            game_representation(players_dictionary)
            print()
            print(f"Player {players_dictionary[player]['color']}: ")
            dice = roll_dice()
            if dice == 6:
                add_pawn(dice, players_dictionary[player], players_dictionary)
            else:
                move_pawn(dice, players_dictionary[player], players_dictionary)
            if check_winner(players_dictionary):
                html.write_map_html(players_dictionary)
                start= False
                break
            html.write_map_html(players_dictionary)

main()