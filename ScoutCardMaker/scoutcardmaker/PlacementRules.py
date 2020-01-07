from Defense import PlacementInfo


def absolute(subformation, arguments):
    if len(arguments) != 2:
        return PlacementInfo(False, None, 'Argument mismatch')
    try:
        x = int(arguments[0])
        y = int(arguments[1])
    except ValueError:
        return PlacementInfo(False, None, 'Argument must be integer numbers')
    return PlacementInfo(True, (x, y), None)


def tech_alignment(subformation, arguments):
    if len(arguments) != 4:
        return PlacementInfo(False, None, 'Argument mismatch')

    technique = arguments[0]
    if technique not in ['0', '1', '2i', '2', '3', '3', '4i', '4', '5', '6i', '6', '7', '8i', '8', '9']:
        return PlacementInfo(False, None, f'{technique} not a defensive technique')

    try:
        depth = int(arguments[1])
    except ValueError:
        return PlacementInfo(False, None, 'Depth must be integer number')

    align_side = arguments[2]
    if align_side not in ['Attached->Receiver', 'Attached', 'Receiver', 'Back']:
        return PlacementInfo(False, None, f'{align_side} Not an align side')

    opposite = arguments[3]
    if opposite not in ['True', 'False']:
        return PlacementInfo(False, None, f'Opposite value must be "True" or "False"')

    return PlacementInfo(True, (5,5), 'Argument mismatch')







placement_rules = {
    'absolute': absolute
}