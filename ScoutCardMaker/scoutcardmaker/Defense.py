from DefensiveConditionParser import condition_parser, placement_parser
from Offense import Formation

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

    def __init__(self):
        self.condition = ''
        self.placement_rule = ''

    def set(self, condition, placement_rule):
        self.condition = condition
        self.placement_rule = placement_rule

    def evaluate_condition(self, subformation):
        #assert ConditionSet.condition_function_map, 'No condition function mapping specified'

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


if __name__ == '__main__':
    from PlacementRules import placement_rules
    ConditionSet.placement_rule_map = placement_rules

    formation = Formation()
    subformation = formation.subformations['MOF_RT']


    # defender = Defender('d1')
    # defender.condition_sets[0].set('Puppy and Kitty("john")', 'absolute 30 20')
    # defender.place(subformation)
    # print(defender)
