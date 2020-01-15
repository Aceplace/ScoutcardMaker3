from Utils import INVALID_POSITION


def absolute(subformation, arguments):
    x = int(arguments[0])
    y = int(arguments[1])
    return x, y


def tech_alignment(subformation, arguments):
    return INVALID_POSITION
#     if len(arguments) != 4:
#         return PlacementInfo(False, None, 'Argument mismatch')
#
#     technique = arguments[0]
#     if technique not in ['0', '1', '2i', '2', '3', '3', '4i', '4', '5', '6i', '6', '7', '8i', '8', '9']:
#         return PlacementInfo(False, None, f'{technique} not a defensive technique')
#
#     try:
#         depth = int(arguments[1])
#     except ValueError:
#         return PlacementInfo(False, None, 'Depth must be integer number')
#
#     align_side = arguments[2]
#     if align_side not in ['Opposite Attached and Receiver', 'Attached', 'Receiver', 'Back', 'Field', 'Boundary', 'LT', 'RT']:
#         return PlacementInfo(False, None, f'{align_side} Not an align side')
#
#     opposite = arguments[3]
#     if opposite not in ['True', 'False']:
#         return PlacementInfo(False, None, f'Opposite value must be "True" or "False"')
#
#     return PlacementInfo(True, (5,5), 'Argument mismatch')


placement_rules = {
    'absolute': absolute,
    'tech_alignment': tech_alignment
}

possible_side_types = ('LT', 'RT', 'Attached', 'Receiver', 'Back', 'Opposite Attached and Receiver', 'Field', 'Boundary')
possible_alignments = ('0', '1', '2i', '2', '3', '3', '4i', '4', '5', '6i', '6', '7', '8i', '8', '9')
possible_bool = ('True', 'False')

placement_rule_info = {
    'absolute': (('int', 'int'), ((), ())),
    'tech_alignment': (('string', 'string', 'int', 'string'), (possible_side_types, possible_alignments, (), possible_bool))
}