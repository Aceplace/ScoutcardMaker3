import unittest
from scoutcardmaker.Defense import Defense
from scoutcardmaker.Offense import Formation
from scoutcardmaker.PlacementRules import first_open_gap
from scoutcardmaker.Utils import INVALID_POSITION


class TestParseValidator(unittest.TestCase):
    def setUp(self):
        pass

    def test_first_pass_return_invalid(self):
        formation = Formation()
        subformation = formation.subformations['MOF_RT']
        defense = Defense()
        defense.pass_number = 1
        position = first_open_gap(subformation, defense, ['Attached', 5, 'False'])
        self.assertEqual(position, INVALID_POSITION)

    def test_first_open_gap_places_correctly_for_over(self):
        formation = Formation()
        subformation = formation.subformations['MOF_RT']
        defense = Defense()
        defense.affected_tags = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']
        defense.players['D1'].placed_x = 6
        defense.players['D1'].placed_y = 1
        defense.players['D2'].placed_x = 12
        defense.players['D2'].placed_y = 1
        defense.players['D3'].placed_x = -2
        defense.players['D3'].placed_y = 1
        defense.players['D4'].placed_x = -10
        defense.players['D4'].placed_y = 1
        defense.pass_number = 2

        defense.players['D5'].placed_x, defense.players['D5'].placed_y = first_open_gap(subformation, defense, ['Attached', 5, 'False'])
        defense.players['D6'].placed_x, defense.players['D6'].placed_y = first_open_gap(subformation, defense, ['Attached', 5, 'True'])

        self.assertEqual(defense.players['D5'].placed_x, 2)
        self.assertEqual(defense.players['D5'].placed_y, 5)
        self.assertEqual(defense.players['D6'].placed_x, -6)
        self.assertEqual(defense.players['D6'].placed_y, 5)

    def test_first_open_gap_places_correctly_for_under(self):
        formation = Formation()
        subformation = formation.subformations['MOF_RT']
        defense = Defense()
        defense.affected_tags = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']
        defense.players['D1'].placed_x = 2
        defense.players['D1'].placed_y = 1
        defense.players['D2'].placed_x = 10
        defense.players['D2'].placed_y = 1
        defense.players['D3'].placed_x = -6
        defense.players['D3'].placed_y = 1
        defense.players['D4'].placed_x = -10
        defense.players['D4'].placed_y = 1
        defense.pass_number = 2

        defense.players['D5'].placed_x, defense.players['D5'].placed_y = first_open_gap(subformation, defense, ['Attached', 5, 'False'])
        defense.players['D6'].placed_x, defense.players['D6'].placed_y = first_open_gap(subformation, defense, ['Attached', 5, 'True'])

        self.assertEqual(defense.players['D5'].placed_x, 6)
        self.assertEqual(defense.players['D5'].placed_y, 5)
        self.assertEqual(defense.players['D6'].placed_x, -2)
        self.assertEqual(defense.players['D6'].placed_y, 5)

    def test_first_open_gap_places_correctly_for_abba(self):
        formation = Formation()
        subformation = formation.subformations['MOF_RT']
        defense = Defense()
        defense.affected_tags = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']
        defense.players['D1'].placed_x = 2
        defense.players['D1'].placed_y = 1
        defense.players['D2'].placed_x = 6
        defense.players['D2'].placed_y = 1
        defense.players['D3'].placed_x = -2
        defense.players['D3'].placed_y = 1
        defense.players['D4'].placed_x = -6
        defense.players['D4'].placed_y = 1
        defense.pass_number = 2

        defense.players['D5'].placed_x, defense.players['D5'].placed_y = first_open_gap(subformation, defense, ['Attached', 5, 'False'])
        defense.players['D6'].placed_x, defense.players['D6'].placed_y = first_open_gap(subformation, defense, ['Attached', 5, 'True'])

        self.assertEqual(defense.players['D5'].placed_x, 10)
        self.assertEqual(defense.players['D5'].placed_y, 5)
        self.assertEqual(defense.players['D6'].placed_x, -10)
        self.assertEqual(defense.players['D6'].placed_y, 5)


