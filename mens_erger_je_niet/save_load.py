def save_game(players_dictionary,player_num):
    with open('game_state.txt','w') as file:
        for i in range(len(players_dictionary)):
            indx = (i + player_num) % len(players_dictionary)
            sentence = ''
            color = players_dictionary[indx]['color']
            available = players_dictionary[indx]['available'] * '/a'
            home = players_dictionary[indx]['home'] * '/h'
            sentence = color + available + home
            for pawn in players_dictionary[indx]['active']:
                sentence += '/'+ str(pawn)
            file.write(sentence+"\n")
            




def load_game(file):
    players_info = {}
    player_num = 0

    for line in file:
        player_info = line.rstrip().split('/')
        color = player_info[0]
        available = player_info.count('a')
        home = player_info.count('h')
        active = [int(num) for num in player_info if num.isdigit()]
        players_info[player_num] = {}
        players_info[player_num]['color'] = color
        players_info[player_num]['available'] = available
        players_info[player_num]['home'] = home
        players_info[player_num]['starting'] = player_num * 10
        players_info[player_num]['active'] = active
        player_num += 1
    return players_info
    