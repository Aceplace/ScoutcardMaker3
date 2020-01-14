import unittest
from DefensiveConditionParser import condition_parser, validate_node, placement_parser, validate_placement_rule


class TestParseValidator(unittest.TestCase):
    inputs_and_expected_outputs = [
        ('func2() <= 10', True, None),
        ('func2() and 10', False, 'func2 returns number when bool expected'),
        ('func2()', False, 'func2 returns number when bool expected'),
        ('func1() and func() > 4', False, 'func1 number of arguments mismatch'),
        ('func1(12, 14) and func1() > 4', False, 'func1 argument mismatch'),
        ('func3(10) = "Jimmy" and (func1(12, "bobby") or func2() > 4)', True, None),
        ('2 and func1(10, "bobby")', False, '2 is number when bool expected'),
        ('func1(12, "jimmy") and func1(10, "bobby")', True, None),
        ('func2() = "joe"', False, 'joe is string when number expected'),
        ('func2() = 10', True, None),
        ('func2() = 10 and func3(11)', False, 'func3 returns string when bool expected'),
        ('func2() = 10 and func3(11) = 12', False, 'func3 returns string when number expected'),
        ('func2() = 10 and func3(11) = "joe"', True, None),
        ('(func2() = 10 and func3(11) = "joe") or func2()', False, 'func2 returns number when bool expected'),
        ('(func2() = 10 and func3(11) = "joe") or func1(13, "oh my")', True, None),
        ('func4("debby", 10, "joe")', True, None),
        ('func4("caesar", 10, "tom")', True, None),
        ('func4("lala", 10, "tom")', False, 'lala is not a valid string input'),
    ]

    formation_function_info = {
        'func1': ('bool', ('number', 'string'), ((), ())),
        'func2': ('number', (), ()),
        'func3': ('string', ('number',), ((),)),
        'func4': ('bool', ('string', 'number', 'string'), (('debby', 'caesar'), (), ()))
    }

    def test_validate_node(self):
        for input_and_expected_output in TestParseValidator.inputs_and_expected_outputs:
            with self.subTest():
                output = validate_node(condition_parser.parse(input_and_expected_output[0]), 'bool', TestParseValidator.formation_function_info)
                self.assertEqual(output[0], input_and_expected_output[1])
                self.assertEqual(output[1], input_and_expected_output[2])


class TestEvaluate(unittest.TestCase):
    inputs_and_expected_outputs = [
        ('func1(0, "bob")', True),
        ('func1(2, "bob")', False),
        ('func2() < 5', True),
        ('func2() < 5', True),
        ('func3("john") = "La: john"', True),
        ('func3("john") = "La-john"', False),
        ('(2 > 4)', False),
        ('(2 < 4)', True),
        ('(2 = 4)', False),
        ('(2 >= 2)', True),
        ('(3 >= 2)', True),
        ('((3 >= 2) and func3("joe") = "3x2")', False),
        ('((3 >= 2) and func3("joe") = "3x2") or 2 = 2', True),
        ('not ((3 >= 2) and func3("joe") = "3x2") or not 2 = 2', True),
        ('not func2() = 2', False)

    ]

    formation_function_map = {
        'func1': lambda subformation, value1, value2: value1 == 0,
        'func2': lambda subformation: 2,
        'func3': lambda subformation, value1: f'La: {value1}'
    }

    def test_evaluate(self):
        for input_and_expected_output in TestEvaluate.inputs_and_expected_outputs:
            with self.subTest():
                root = condition_parser.parse(input_and_expected_output[0])
                output = root.evaluate(None, TestEvaluate.formation_function_map)
                self.assertEqual((input_and_expected_output[0], output), (input_and_expected_output[0], input_and_expected_output[1]))



class TestPlacementValidator(unittest.TestCase):
    inputs_and_expected_outputs = [
        ('rule_doesnt_exist blah', False, 'rule_doesnt_exist is not a placement rule'),
    ]

    placement_rule_info = {
        'rule_1': ((),()),
        'rule_2': ((),()),
        'rule_3': ((),()),
    }

    def test_evaluate(self):
        for input_and_expected_output in TestPlacementValidator.inputs_and_expected_outputs:
            with self.subTest():
                parsed_placement_rule = placement_parser.parse(input_and_expected_output[0])
                output = validate_placement_rule(parsed_placement_rule[0], parsed_placement_rule[1], TestPlacementValidator.placement_rule_info)
                self.assertEqual((input_and_expected_output[0], output[0], output[1]),
                                 (input_and_expected_output[0], input_and_expected_output[1], input_and_expected_output[2]))


if __name__ == '__main__':
    unittest.main()
