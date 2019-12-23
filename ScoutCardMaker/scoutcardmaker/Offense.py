import json


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
        self.players = [
            Player('L1', 0, 0),
            Player('L2', 0, 0),
            Player('L3', 0, 0),
            Player('L4', 0, 0),
            Player('C', 0, 0),
            Player('S1', 0, 0),
            Player('S2', 0, 0),
            Player('S3', 0, 0),
            Player('S4', 0, 0),
            Player('S5', 0, 0),
            Player('S6', 0, 0),
        ]

    def __repr__(self):
        player_strings = ',\n'.join(str(player) for player in self.players)
        return f'Subformation(\n[{player_strings}]\n)'

    def to_dict(self):
        players_as_dicts = [player.to_dict() for player in self.players]
        return {
            'players': players_as_dicts
        }

    @staticmethod
    def from_dict(obj):
        subformation = Subformation()
        players_list = [Player(player['tag'], player['x'], player['y']) for player in obj['players']]
        subformation.players = players_list
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
# with open('file2.json', 'r') as file:
#     library = OffenseLibrary.from_dict(json.load(file))
#
# print(library)