import json
import scoutcardmaker.SubformationUtils as su
from scoutcardmaker.Offense import Formation

######################
# This exporter is meant to be used with my football trainer program, and its format matches what is expected by that.
#####################
def export_to_football_trainer(file_name, plays, offense_library, defense_library):
    script_plays = []
    default_subformation = Formation().subformations['MOF_RT']
    for play in plays:
        offense_info = f'{play["Number"]} {play["Personnel"]} {play["Hash"]} {play["Dnd"]} {play["Formation"]} {play["Play"]}'
        defense_info = f'{play["Defense"]} --- {play["Note"]}'


        play_dict = {'offenseInfo': offense_info, 'defenseInfo': defense_info}
        formation_name = play["Card Maker Formation"]
        defense_name = play["Card Maker Defense"]
        subformation, error_message = offense_library.get_composite_subformation(play['Hash'], formation_name)

        if not subformation:
            subformation = default_subformation

        if subformation.hash_mark == 'LT':
            hash_type = 0
        elif subformation.hash_mark == 'MOF':
            hash_type = 1
        else:
            hash_type = 2
        play_dict['hashType'] = hash_type

        players = []
        for tag, player in subformation.players.items():
            player_dict = {'tag': tag, 'pose': determine_pose(player, subformation), 'x': player.x, 'y': player.y}
            players.append(player_dict)

        composite_defense = defense_library.get_composite_defense(defense_name)
        composite_defense.place_defenders(subformation)
        for tag, defender in composite_defense.players.items():
            player_dict = {'tag': tag, 'pose': determine_pose(defender, subformation), 'x': defender.placed_x, 'y': -defender.placed_y}
            players.append(player_dict)

        play_dict['players'] = players
        script_plays.append(play_dict)

    script = {'plays': script_plays}

    with open(file_name, 'w') as file:
        json.dump(script, file, indent=3)


def determine_pose(player, subformation):
    if player.tag in ['L1', 'L2', 'L3', 'L4', 'C', 'D1', 'D2', 'D3', 'D4']:
        return 'linemanStance'

    if player.tag in ['D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11']:
        return 'rbStance'

    if player.tag == 'S1':
        return 'qbStance' if player.y == 2 else 'qbStanceGun'

    subformation_players = list(subformation.players.values())
    backfield_players = su.get_backfield_ordered(subformation_players)
    detached_players = su.get_detached_skill_ordered(subformation_players)

    if player in backfield_players:
        return 'rbStance'
    if player in detached_players:
        return 'wrStance'

    stance_threshold = 5
    if player.y == 1 and player.x <= su.get_rt(subformation_players).x + stance_threshold:
        return 'linemanStance'
    if player.y == 1 and player.x >= su.get_lt(subformation_players).x - stance_threshold:
        return 'linemanStance'
    return 'rbStance'

