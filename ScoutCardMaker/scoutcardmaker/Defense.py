from DefensiveConditionParser import condition_parser, placement_parser
from Offense import Formation

INVALID_POSITION = (-100, -100)

class ConditionSet:
    def __init__(self):
        self.condition = ''
        self.placement_rule = ''

    def set(self, condition, placement_rule):
        self.condition = condition
        self.placement_rule = placement_rule

    def evaluate_condition(self, subformation):
        if len(self.condition) == 0:
            return True
        else:
            return False

    def get_placement(self, subformation):
        parsed_placement_rule = placement_parser.parse(self.placement_rule)
        placement_rule_name = parsed_placement_rule[0]
        arguments = parsed_placement_rule[1]
        try:
            return placement_rules[placement_rule_name](subformation, arguments)
        except KeyError:
            return PlacementInfo(False, None, f'Placement Rule "{placement_rule_name}" doesn\'t exist')

    def __repr__(self):
        return f'CondSet({self.condition}, {self.placement_rule})'


class Defender:
    def __init__(self, tag):
        self.tag = tag
        self.condition_sets = [ConditionSet()]
        self.placed_x, self.placed_y = INVALID_POSITION

    def place(self, subformation):
        for condition_set in self.condition_sets:
            if condition_set.evaluate_condition(subformation):
                placement_info = condition_set.get_placement(subformation)
                if placement_info.success:
                    self.placed_x, self.placed_y = placement_info.position
                    return
                else:
                    break
        self.placed_x, self.placed_y = INVALID_POSITION

    def __repr__(self):
        condition_set_strings = '\n'.join([repr(condition_set) for condition_set in self.condition_sets])
        return f'Defender({self.tag}, {self.placed_x}, {self.placed_y}, [{condition_set_strings}])'


class PlacementInfo:
    def __init__(self, success, position, error_message=None):
        self.success = success
        self.position = position
        self.error_message = error_message

    def __repr__(self):
        return f'PlacementInfo({(self.success, self.position, self.error_message)})'


def absolute(subformation, arguments):
    if len(arguments) != 2:
        return PlacementInfo(False, None, 'Argument mismatch')
    try:
        x = int(arguments[0])
        y = int(arguments[1])
    except ValueError:
        return PlacementInfo(False, None, 'Argument must be integer numbers')
    return PlacementInfo(True, (x, y), 'Argument mismatch')

placement_rules = {
    'absolute': absolute
}


if __name__ == '__main__':
    formation = Formation()
    subformation = formation.subformations['MOF_RT']

    defender = Defender('d1')
    defender.condition_sets[0].set('', 'absolute 10 20')
    defender.place(subformation)
    print(defender)
