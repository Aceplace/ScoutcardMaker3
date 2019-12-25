import copy

class Player:
    def __init__(self, tag, x, y):
        self.tag = tag
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Player({self.tag},{self.x},{self.y})'

    def to_dict(self):
        return {
            'tag': self.tag,
            'x': self.x,
            'y': self.y
        }

    @staticmethod
    def from_dict(obj):
        return Player(obj['tag'], obj['x'], obj['y'])


class Subformation:
    def __init__(self):
        self.players = {
            'L1': Player('L1', 0, 1),
            'L2': Player('L2', 0, 1),
            'L3': Player('L3', 0, 1),
            'L4': Player('L4', 0, 1),
            'C': Player('C', 0, 1),
            'S1': Player('S1', 0, 1),
            'S2': Player('S2', 0, 1),
            'S3': Player('S3', 0, 1),
            'S4': Player('S4', 0, 1),
            'S5': Player('S5', 0, 1),
            'S6': Player('S6', 0, 1),
        }

    def copy_from(self, subformation):
        self.players = copy.deepcopy(subformation.players)

    def copy_affected(self, subformation, affected_player_tags):
        for key, player in self.players.items():
            if player.tag in affected_player_tags:
                self.players[key] = copy.deepcopy(subformation.players[key])

    def flip(self):
        self.players['L1'].x, self.players['L4'].x = self.players['L4'].x, self.players['L1'].x
        self.players['L2'].x, self.players['L3'].x = self.players['L3'].x, self.players['L2'].x
        for player in self.players.values():
            player.x *= -1

    def __repr__(self):
        player_strings = ',\n'.join(str(player) for player in self.players.values())
        return f'Subformation(\n[{player_strings}]\n)'

    def to_dict(self):
        players_as_dicts = {key: player.to_dict() for (key, player) in self.players.items()}
        return {
            'players': players_as_dicts
        }

    @staticmethod
    def from_dict(obj):
        subformation = Subformation()
        players_dict = {key: Player(player['tag'], player['x'], player['y']) for (key, player) in obj['players'].items()}
        subformation.players = players_dict
        return subformation


class Formation:
    def __init__(self):
        self.subformations = {
            'MOF_RT': Subformation(),
            'LH_RT': Subformation(),
            'RH_RT': Subformation(),
            'MOF_LT': Subformation(),
            'LH_LT': Subformation(),
            'RH_LT': Subformation(),
        }
        default_subformations = {'L1': (-8, 1), 'L2': (-4, 1), 'L3': (4, 1), 'L4': (8, 1), 'C': (0, 1),
                                       'S1': (0, 2), 'S2': (0, 7), 'S3': (0, 5), 'S4': (-36, 1), 'S5': (12, 1),
                                       'S6': (36, 2)}
        for tag, position in default_subformations.items():
            self.subformations['MOF_RT'].players[tag].x = position[0]
            self.subformations['MOF_RT'].players[tag].y = position[1]

        default_subformations = {'L1': (-26, 1), 'L2': (-22, 1), 'L3': (-14, 1), 'L4': (-10, 1), 'C': (-18, 1),
                                       'S1': (-18, 2), 'S2': (-18, 7), 'S3': (-18, 5), 'S4': (-44, 1), 'S5': (-6, 1),
                                       'S6': (20, 2)}
        for tag, position in default_subformations.items():
            self.subformations['LH_RT'].players[tag].x = position[0]
            self.subformations['LH_RT'].players[tag].y = position[1]

        default_subformations = {'L1': (10, 1), 'L2': (14, 1), 'L3': (22, 1), 'L4': (26, 1), 'C': (18, 1),
                                       'S1': (18, 2), 'S2': (18, 7), 'S3': (18, 5), 'S4': (-20, 1), 'S5': (30, 1),
                                       'S6': (44, 2)}
        for tag, position in default_subformations.items():
            self.subformations['RH_RT'].players[tag].x = position[0]
            self.subformations['RH_RT'].players[tag].y = position[1]

        self.auto_gen_going_left_from_right()

        self.affected_tags = []

    def copy_from(self, formation):
        self.subformations = copy.deepcopy(formation.subformations)
        self.affected_tags = copy.deepcopy(formation.affected_tags)

    def auto_gen_going_left_from_right(self):
        self.subformations['MOF_LT'].copy_from(self.subformations['MOF_RT'])
        self.subformations['MOF_LT'].flip()
        self.subformations['LH_LT'].copy_from(self.subformations['RH_RT'])
        self.subformations['LH_LT'].flip()
        self.subformations['RH_LT'].copy_from(self.subformations['LH_RT'])
        self.subformations['RH_LT'].flip()

    def __repr__(self):
        subformation_strings = ',\n'.join(f'{key}:{item}' for (key,item) in self.subformations.items())
        return f'Formation({subformation_strings}, Affected Tags: {self.affected_tags}'

    def to_dict(self):
        subformations_as_dicts = {key: item.to_dict() for (key, item) in self.subformations.items()}
        return {
            'subformations': subformations_as_dicts,
            'affected_tags': self.affected_tags
        }

    @staticmethod
    def from_dict(obj):
        formation = Formation()
        formation.subformations = {key: Subformation.from_dict(item) for (key, item) in obj['subformations'].items()}
        formation.affected_tags = obj['affected_tags']
        return formation


class PersonnelLabelMapper:
    def __init__(self):
        self.mappings = {'L1': 'LT',
                         'L2': 'LG',
                         'L3': 'RG',
                         'L4': 'RT',
                         'C': 'C',
                         'S1': 'Q',
                         'S2': 'T',
                         'S3': 'H',
                         'S4': 'X',
                         'S5': 'Y',
                         'S6': 'Z'}

    def get_label(self, tag):
        return self.mappings[tag]

    def to_dict(self):
        return self.mappings

    def __repr__(self):
        return f'Personnel Mapper({self.mappings})'

    @staticmethod
    def from_dict(obj):
        label_mapper = PersonnelLabelMapper()
        label_mapper.mappings = obj
        return label_mapper




class OffenseLibrary:
    Default_Formation = Formation()

    def __init__(self):
        self.formations = {}
        self.label_mappers = {'default': PersonnelLabelMapper()}

    def save_formation(self, formation, name):
        formation_name = name.upper().strip().split()
        if 'LT' in formation_name or 'RT' in formation_name:
            return False

        formation_name = ' '.join(formation_name)

        new_formation = Formation()
        new_formation.copy_from(formation)

        self.formations[formation_name] = new_formation
        return True

    def save_formation_from_going_rt(self, formation, name):
        formation_name = name.upper().strip().split()
        if 'LT' in formation_name or 'RT' in formation_name:
            return False

        formation_name = ' '.join(formation_name)

        new_formation = Formation()
        new_formation.copy_from(formation)
        new_formation.auto_gen_going_left_from_right()

        self.formations[formation_name] = new_formation
        return True

    def get_composite_subformation(self, hash, name):
        formation_words = name.strip().upper().split()
        if len(formation_words) < 2:
            return (None, 'Formation name requires at least two words')
        if formation_words.count('RT') + formation_words.count('LT') > 1:
            return (None, 'Formation can\'t specify a direction twice')
        elif 'RT' in formation_words:
            formation_direction = 'RT'
        elif 'LT' in formation_words:
            formation_direction = 'LT'
        else:
            return (None, 'Formation requires direction')

        subformation_to_return = Subformation()
        subformation_to_return.copy_from(OffenseLibrary.Default_Formation.subformations[f'{hash}_{formation_direction}'])

        # start_index = 0
        # current_index = 0
        # match_index = 0
        # matching_formation_name = ''
        # while start_index < len(formation_words):
        #     if current_index >= len(formation_words) or formation_words[current_index] in ['LT', 'RT']:
        #         if len(matching_formation_name) == 0:
        #             return (None, f'Formation {name} not found in library.')
        #         else:
        #             subformation_to_copy = self.formations[matching_formation_name].subformations[f'{hash}_{formation_direction}']
        #             affected_players = self.formations[matching_formation_name].affected_tags
        #             subformation_to_return.copy_affected(subformation_to_copy, affected_players)
        #             start_index = match_index + 1
        #             current_index = match_index + 1
        #             matching_formation_name = ''
        #     if formation_words[current_index] in ['LT', 'RT'] and current_index == start_index:
        #         start_index += 1
        #         current_index += 1
        #         continue
        #     subformation_name = ' '.join(formation_words[start_index: current_index + 1])
        #     if subformation_name in self.formations:
        #         match_index = current_index
        #         matching_formation_name = subformation_name
        #     current_index += 1
        matches = []
        direction_index = formation_words.index(formation_direction)
        words_1, words_2 = formation_words[0: direction_index], formation_words[direction_index + 1:]

        if len(words_1) > 0:
            start_index = 0
            end_index = len(words_1)

            while start_index < len(words_1):
                subformation_name = ' '.join(words_1[start_index:end_index])
                if subformation_name in self.formations:
                    matches.append(subformation_name)
                    start_index = end_index
                    end_index = len(words_1)
                else:
                    end_index -= 1
                    if end_index == start_index:
                        return (None, f'Formation {name} not found in library.')

        if len(words_2) > 0:
            start_index = 0
            end_index = len(words_2)

            while start_index < len(words_2):
                subformation_name = ' '.join(words_2[start_index:end_index])
                if subformation_name in self.formations:
                    matches.append(subformation_name)
                    start_index = end_index
                    end_index = len(words_2)
                else:
                    end_index -= 1
                    if end_index == start_index:
                        return (None, f'Formation {name} not found in library.')

        for match in matches:
            subformation_to_copy = self.formations[match].subformations[ f'{hash}_{formation_direction}']
            affected_players = self.formations[match].affected_tags
            subformation_to_return.copy_affected(subformation_to_copy, affected_players)

        return (subformation_to_return, None)

    def __repr__(self):
        return f'OffenseLibrary(Formations({self.formations}), Personnel Groups({self.label_mappers}))'

    def to_dict(self):
        formations_as_dicts = {key: item.to_dict() for (key, item) in self.formations.items()}
        return {
            'formations': formations_as_dicts,
            'label_mappers': {key: item.to_dict() for (key, item) in self.label_mappers.items()}
        }

    @staticmethod
    def from_dict(obj):
        library = OffenseLibrary()
        library.formations = {key: Formation.from_dict(item) for (key, item) in obj['formations'].items()}
        library.label_mappers = {key: PersonnelLabelMapper.from_dict(item) for (key, item) in obj['label_mappers'].items()}
        return library

import json
# with open('file.json', 'r') as file:
#     formation = Formation.from_dict(json.load(file))
#
# print(formation)

# with open('file2.json', 'w') as file:
#     library = OffenseLibrary()
#     library.formations['Pro'] = Formation()
#     library.formations['Twin'] = Formation()
#     json.dump(library.to_dict(), file, indent=4)
#
# with open('library.json', 'r') as file:
#     library = OffenseLibrary.from_dict(json.load(file))
#
# print(library.get_composite_subformation('MOF', 'Twin-Tight King Rt'))