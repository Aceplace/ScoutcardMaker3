import SubformationUtils as su


def formation_structure(subformation):
    return su.get_formation_structure(subformation.players)


def num_receivers(subformation, side_type):
    side = su.get_side(side_type, subformation.players, subformation.hash_mark)
    return su.get_num_receivers(subformation.players, side)


def num_attached(subformation, side_type):
    side = su.get_side(side_type, subformation.players, subformation.hash_mark)
    return su.get_num_attached(subformation.players, side)


def num_detached(subformation, side_type):
    side = su.get_side(side_type, subformation.players, subformation.hash_mark)
    return su.get_num_detached(subformation.players, side)


def surface(subformation, side_type):
    side = su.get_side(side_type, subformation.players, subformation.hash_mark)
    return su.get_surface_structure(subformation.players, side)


def ball_on_hash(subformation):
    return subformation.hash_mark in ['LT', 'RT']


def ball_in_middle(subformation):
    return subformation.hash_mark == 'MOF'


def ball(subformation):
    assert subformation.hash_mark in ['LT', 'RT', 'MOF']
    return subformation.hash_mark


formation_function_map = {
    'formation_structure': formation_structure,
    'num_receivers': num_receivers,
    'num_attached': num_attached,
    'num_detached': num_detached,
    'surface': surface,
    'ball_on_hash': ball_on_hash,
    'ball_in_middle': ball_in_middle,
    'ball': ball,
}


possible_side_types = ('LT', 'RT', 'Attached', 'Receiver', 'Back', 'Opposite Attached and Receiver', 'Field', 'Boundary')

formation_function_info = {
    'formation_structure': ('string', (), (possible_side_types,)),
    'num_receivers': ('number', ('string',), (possible_side_types,)),
    'num_attached': ('number', ('string',), (possible_side_types,)),
    'num_detached': ('number', ('string',), (possible_side_types,)),
    'surface': ('string', ('string',), (possible_side_types,)),
    'ball_on_hash': ('bool', (), ()),
    'ball_in_middle': ('bool', (), ()),
    'ball': ('string', (), ()),
}