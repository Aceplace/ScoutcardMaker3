from Defense import  PlacementInfo

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