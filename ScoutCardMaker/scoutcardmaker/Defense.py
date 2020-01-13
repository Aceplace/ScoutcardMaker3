from DefensiveConditionParser import condition_parser, placement_parser
from Offense import Formation
from LibraryUtils import PersonnelLabelMapper
import copy

INVALID_POSITION = (-100, -100)

class ConditionInfo:
    def __init__(self, success, value, error_message):
        self.success = success
        self.value = value
        self.error_message = error_message

    def __repr__(self):
        return f'ConditionInfo({(self.success, self.value, self.error_message)})'

class PlacementInfo:
    def __init__(self, success, position, error_message=None):
        self.success = success
        self.position = position
        self.error_message = error_message

    def __repr__(self):
        return f'PlacementInfo({(self.success, self.position, self.error_message)})'

class ConditionSet:
    placement_rule_map = None
    condition_function_map = None

    def __init__(self, condition='', placement_rule=''):
        self.condition = condition
        self.placement_rule = placement_rule

    def set(self, condition, placement_rule):
        self.condition = condition
        self.placement_rule = placement_rule

    def evaluate_condition(self, subformation):
        # assert ConditionSet.condition_function_map, 'No condition function mapping specified'

        if len(self.condition) == 0:
            return ConditionInfo(True, True, None)

        try:
            parsed_condition_tree = condition_parser.parse(self.condition)
        except ValueError as e:
            return ConditionInfo(False, False, f'Parse error:{e}')

        return ConditionInfo(True, True, None)

    def get_placement(self, subformation):
        assert ConditionSet.placement_rule_map,  'No placement rule mapping specified'

        parsed_placement_rule = placement_parser.parse(self.placement_rule)
        placement_rule_name = parsed_placement_rule[0]
        arguments = parsed_placement_rule[1]
        try:
            return placement_rules[placement_rule_name](subformation, arguments)
        except KeyError:
            return PlacementInfo(False, None, f'Placement Rule "{placement_rule_name}" doesn\'t exist')

    def __repr__(self):
        return f'CondSet({self.condition}, {self.placement_rule})'

    def to_dict(self):
        return {
            'condition': self.condition,
            'placement_rule': self.placement_rule
        }

    @staticmethod
    def from_dict(obj):
        condition_set = ConditionSet()
        condition_set.condition = obj['condition_set']
        condition_set.placement_rule = obj['placement_rule']
        return condition_set


class Defender:
    def __init__(self, tag):
        self.tag = tag
        self.condition_sets = [ConditionSet()]
        self.placed_x, self.placed_y = INVALID_POSITION

    def place(self, subformation):
        for condition_set in self.condition_sets:
            condition_info = condition_set.evaluate_condition(subformation)
            if not condition_info.success:
                print(f'Couldn\t evaluate condition: {condition_info.error_message}')
                continue
            if condition_info.value:
                placement_info = condition_set.get_placement(subformation)
                if placement_info.success:
                    self.placed_x, self.placed_y = placement_info.position
                    return
                else:
                    print(f'Couldn\'t place: {placement_info.error_message}')
                    break
        self.placed_x, self.placed_y = INVALID_POSITION

    def __repr__(self):
        condition_set_strings = '\n'.join([repr(condition_set) for condition_set in self.condition_sets])
        return f'Defender({self.tag}, {self.placed_x}, {self.placed_y}, [{condition_set_strings}])'

    def to_dict(self):
        condition_sets_as_dicts = [condition_set.to_dict() for condition_set in self.condition_sets]
        return {
            'tag': self.tag,
            'condition_sets': condition_sets_as_dicts
        }

    @staticmethod
    def from_dict(obj):
        defender = Defender(obj['tag'])
        condition_sets = [ConditionSet(condition_set['condition'], condition_set['placement_rule']) for
                          condition_set in obj['condition_sets']]
        defender.condition_sets = condition_sets
        return defender


class Defense:
    def __init__(self):
        self.players = {
            'D1': Defender('D1'),
            'D2': Defender('D2'),
            'D3': Defender('D3'),
            'D4': Defender('D4'),
            'D5': Defender('D5'),
            'D6': Defender('D6'),
            'D7': Defender('D7'),
            'D8': Defender('D8'),
            'D9': Defender('D9'),
            'D10': Defender('D10'),
            'D11': Defender('D11'),
        }
        self.affected_tags = []

    def copy_from(self, defense):
        self.players = copy.deepcopy(defense.players)
        self.affected_tags = copy.deepcopy(defense.affected_tags)

    def copy_affected(self, defense, affected_player_tags):
        for key, player in self.players.items():
            if player.tag in affected_player_tags:
                self.players[key] = copy.deepcopy(defense.players[key])

    def __repr__(self):
        player_strings = ',\n'.join(str(player) for player in self.players.values())
        return f'Defense(\n[{player_strings}]\n)'

    def to_dict(self):
        players_as_dicts = {key: player.to_dict() for (key, player) in self.players.items()}
        return {
            'players': players_as_dicts,
            'affected_tags': self.affected_tags
        }

    @staticmethod
    def from_dict(obj):
        defense = Defense()
        players_dict = {key: Defender.from_dict(player) for (key, player) in obj['players'].items()}
        defense.players = players_dict
        defense.affected_tags = obj['affected_tags']
        return defense


class DefenseLibrary:
    def __init__(self):
        self.defenses = {}
        self.label_mappers = {'default': PersonnelLabelMapper('defense')}


    def save_defense(self, defense, name):
        defense_name = name.upper().strip().split()
        defense_name = ' '.join(defense_name)

        new_defense = Defense()
        new_defense.copy_from(defense)

        self.defenses[defense_name] = new_defense
        return True


    def get_composite_defense(self, name):
        defense_words = name.strip().upper().split()

        defense_to_return = Defense()

        matches = []

        start_index = 0
        end_index = len(defense_words)
        while start_index < len(defense_words):
            subdefense_name = ' '.join(defense_words[start_index:end_index])
            if subdefense_name in self.defense:
                matches.append(subdefense_name)
                start_index = end_index
                end_index = len(defense_words)
            else:
                end_index -= 1
                if end_index == start_index:
                    start_index += 1
                    end_index = len(defense_words)


        for match in matches:
            subdefense_to_copy = self.defenses[match]
            affected_players = self.defenses[match].affected_tags
            defense_to_return.copy_affected(subdefense_to_copy, affected_players)

        return defense_to_return

    def __repr__(self):
        return f'DefenseLibrary(Defenses({self.defenses}), Personnel Groups({self.label_mappers}))'

    def to_dict(self):
        defenses_as_dicts = {key: item.to_dict() for (key, item) in self.defenses.items()}
        return {
            'defenses': defenses_as_dicts,
            'label_mappers': {key: item.to_dict() for (key, item) in self.label_mappers.items()}
        }

    @staticmethod
    def from_dict(obj):
        library = DefenseLibrary()
        library.defenses = {key: Defense.from_dict(item) for (key, item) in obj['defenses'].items()}
        library.label_mappers = {key: PersonnelLabelMapper.from_dict(item) for (key, item) in obj['label_mappers'].items()}
        return library


if __name__ == '__main__':
    from PlacementRules import placement_rules
    ConditionSet.placement_rule_map = placement_rules

    formation = Formation()
    subformation = formation.subformations['MOF_RT']


    # defender = Defender('d1')
    # defender.condition_sets[0].set('Puppy and Kitty("john")', 'absolute 30 20')
    # defender.place(subformation)
    # print(defender)
