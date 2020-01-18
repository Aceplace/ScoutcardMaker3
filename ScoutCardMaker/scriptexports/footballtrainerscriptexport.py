import json

def export_to_football_trainer(file_name, plays, offense_library, defense_library):

    script = []
    for play in plays:
        offense_info = f'{play["Number"]} {play["Personnel"]} {play["Hash"]} {play["Dnd"]} {play["Formation"]} {play["Play"]}'
        defense_info = f'{play["Defense"]} --- {play["Note"]}'
        play_dict = {'offense_info': offense_info, 'defense_info': defense_info, 'offense': None, 'defense': None}
        formation_name = play["Card Maker Formation"]
        defense_name = play["Card Maker Defense"]
        subformation, error_message = offense_library.get_composite_subformation(play['Hash'], formation_name)
        if subformation:
            offense = {}
            for tag, player in subformation.players.items():
                offense[tag] = [player.x, player.y]
            play_dict['offense'] = offense

            composite_defense = defense_library.get_composite_defense(defense_name)
            composite_defense.place_defenders(subformation)
            defense = {}
            for tag, defender in composite_defense.players.items():
                defense[tag] = [defender.placed_x, defender.placed_y]
            play_dict['defense'] = defense
        script.append(play_dict)

    with open(file_name, 'w') as file:
        json.dump(script, file, indent=3)
