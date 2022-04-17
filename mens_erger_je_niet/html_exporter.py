HTML_EXPORT_FILE = "template/index.html"

def export(body):
    output = f"""<!Doctype html>
    <html>
    <head>
        <title>Pawn Killer game</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <table class="field">
        {body}
        </table>
    </body>
    </html>
    """
    with open(HTML_EXPORT_FILE,'w') as file:
        file.write(output)


def write_map_html(players_dictionary):
    rows = 11
    columns = 11
    the_map = ''

    gameBoardID = {
        0: 6, 1: 17,2: 28,3: 39,4: 50,5: 51,6: 52,7: 53,8: 54,9: 65,10: 76,11: 75,
        12: 74,13: 73,14: 72,15: 83,16: 94,17: 105,18: 116,19: 115,20: 114,
        21: 103,22: 92,23: 81,24: 70,25: 69,26: 68,27: 67,28: 66,
        29: 55,30: 44,31: 45,32: 46,33: 47,34: 48,35: 37,36: 26,
        37: 15,38: 4, 39: 5
    }
    quarters_pos = {0:[9, 10, 20, 21],
                    1:[108, 109, 119, 120],
                    2:[99, 100, 110, 111],
                    3:[0, 1, 11, 12]
                    }
    home_pos = {
        0:[49,38,27,16],
        1:[61,62,63,64],
        2:[71,82,93,104],
        3:[59,58,57,56]
    }
    for player in players_dictionary:
        players_dictionary[player]['board_position'] = []
        players_dictionary[player]['quarters'] = quarters_pos[player]
        players_dictionary[player]['home_board_position'] = home_pos[player]
        for pos in players_dictionary[player]['active']:
            players_dictionary[player]['board_position'].append(gameBoardID[pos])
    
    map_position = {
        44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 65, 55, 4, 6, 15, 17, 26, 28, 37, 39,
        66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 81, 83, 92, 94, 103, 105, 114, 116}
    home_position = {5, 38, 71, 104, 16, 49, 82, 115,
                        27, 93, 56, 57, 58, 59, 61, 62, 63, 64}
    rest_place = {9, 10, 20, 21, 0, 1, 11, 12,
                    108, 109, 119, 120, 99, 100, 110, 111}

    circle_id = 0
    for row in range(0,rows):
        the_map += '''<tr>
        '''
        for column in range(0,columns):
            id_found = False
            if not circle_id in rest_place and circle_id not in map_position and circle_id not in home_position:
                the_map += f"""<td class="point" id="{circle_id}" style="border:none"></td>
                """
            else:
                for place in players_dictionary:                            
                    if circle_id in players_dictionary[place]['quarters'][:players_dictionary[place]['available']]:
                        the_map += f"""<td class="point" id="{circle_id}" style="background-color:{players_dictionary[place]['color']}"></td>
                        """
                        break
                else:
                    for player in players_dictionary:
                        if circle_id in players_dictionary[player]['board_position'] or circle_id in players_dictionary[player]['home_board_position'][:players_dictionary[player]['home']]:
                            the_map += f"""<td class="point" id="{circle_id}" style="background-color:{players_dictionary[player]['color']}; box-shadow:2px 2px red;"></td>
                            """
                            id_found = True
                    if id_found == False:
                        the_map += f"""<td class="point" id="{circle_id}" style="box-shadow: 2px 2px red;"></td>
                        """
            circle_id += 1
        the_map+= """</tr>
            """
    
    export(the_map)        