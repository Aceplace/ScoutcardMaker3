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
            'L1': Player('L1', 0, 0),
            'L2': Player('L2', 0, 0),
            'L3': Player('L3', 0, 0),
            'L4': Player('L4', 0, 0),
            'C': Player('C', 0, 0),
            'S1': Player('S1', 0, 0),
            'S2': Player('S2', 0, 0),
            'S3': Player('S3', 0, 0),
            'S4': Player('S4', 0, 0),
            'S5': Player('S5', 0, 0),
            'S6': Player('S6', 0, 0),
        }

    def copy_from(self, subformation):
        self.players = copy.deepcopy(subformation.players)

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
        test_subformation_positions = {'L1': (-8, 0), 'L2': (-4, 0), 'L3': (4, 0), 'L4': (8, 0), 'C': (0, 0),
                                       'S1': (0, 1), 'S2': (0, 4), 'S3': (0, 6), 'S4': (12, 0), 'S5': (-36, 0),
                                       'S6': (36, 1)}
        for tag, position in test_subformation_positions.items():
            self.subformations['MOF_RT'].players[tag].x = position[0]
            self.subformations['MOF_RT'].players[tag].y = position[1]

        test_subformation_positions = {'L1': (-26, 0), 'L2': (-22, 0), 'L3': (-14, 0), 'L4': (-10, 0), 'C': (-18, 0),
                                       'S1': (-18, 1), 'S2': (-18, 4), 'S3': (-18, 6), 'S4': (-6, 0), 'S5': (-44, 0),
                                       'S6': (20, 1)}
        for tag, position in test_subformation_positions.items():
            self.subformations['LH_RT'].players[tag].x = position[0]
            self.subformations['LH_RT'].players[tag].y = position[1]

        test_subformation_positions = {'L1': (10, 0), 'L2': (14, 0), 'L3': (22, 0), 'L4': (26, 0), 'C': (18, 0),
                                       'S1': (18, 1), 'S2': (18, 4), 'S3': (18, 6), 'S4': (30, 0), 'S5': (-20, 0),
                                       'S6': (44, 1)}
        for tag, position in test_subformation_positions.items():
            self.subformations['RH_RT'].players[tag].x = position[0]
            self.subformations['RH_RT'].players[tag].y = position[1]

        self.subformations['MOF_LT'].copy_from(self.subformations['MOF_RT'])
        self.subformations['MOF_LT'].flip()
        self.subformations['LH_LT'].copy_from(self.subformations['RH_RT'])
        self.subformations['LH_LT'].flip()
        self.subformations['RH_LT'].copy_from(self.subformations['LH_RT'])
        self.subformations['RH_LT'].flip()

        self.affected_tags = []

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
                         'L4': 'RG',
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
    def __init__(self):
        self.formations = {}
        self.label_mappers = {'default': PersonnelLabelMapper()}


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

# with open('file2.json', 'r') as file:
#     library = OffenseLibrary.from_dict(json.load(file))
#
# print(library)