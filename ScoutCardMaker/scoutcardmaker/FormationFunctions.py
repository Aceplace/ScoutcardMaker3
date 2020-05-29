import scoutcardmaker.SubformationUtils as su


def formation_structure(subformation):
    return su.get_formation_structure(list(subformation.players.values()))


def num_receivers(subformation, side_type, flip):
    side = su.get_side(side_type, list(subformation.players.values()), subformation.hash_mark)
    if flip == 'True':
        side = 'RT' if side == 'LT' else 'LT'
    return su.get_num_receivers(list(subformation.players.values()), side)

def num_backs(subformation):
    return len(su.get_backfield_ordered(list(subformation.players.values()))) - 1

def num_attached(subformation, side_type, flip):
    side = su.get_side(side_type, list(subformation.players.values()), subformation.hash_mark)
    if flip == 'True':
        side = 'RT' if side == 'LT' else 'LT'
    return su.get_num_attached(list(subformation.players.values()), side)

def num_detached(subformation, side_type, flip):
    side = su.get_side(side_type, list(subformation.players.values()), subformation.hash_mark)
    if flip == 'True':
        side = 'RT' if side == 'LT' else 'LT'
    return su.get_num_detached(list(subformation.players.values()), side)

def is_there_te(subformation, side_type, flip):
    side = su.get_side(side_type, list(subformation.players.values()), subformation.hash_mark)
    if flip == 'True':
        side = 'RT' if side == 'LT' else 'LT'
    first_attached = su.get_first_attached(list(subformation.players.values()), side)
    return first_attached != None and first_attached.y == 1

def surface(subformation, side_type, flip):
    side = su.get_side(side_type, list(subformation.players.values()), subformation.hash_mark)
    if flip == 'True':
        side = 'RT' if side == 'LT' else 'LT'
    return su.get_surface_structure(list(subformation.players.values()), side)

def num_offset_backs(subformation, side_type, flip):
    side = su.get_side(side_type, list(subformation.players.values()), subformation.hash_mark)
    if flip == 'True':
        side = 'RT' if side == 'LT' else 'LT'
    return su.get_num_offset_backs(list(subformation.players.values()), side)


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
    'num_backs': num_backs,
    'num_attached': num_attached,
    'num_detached': num_detached,
    'surface': surface,
    'ball_on_hash': ball_on_hash,
    'ball_in_middle': ball_in_middle,
    'ball': ball,
    'is_there_te': is_there_te,
    'num_offset_backs': num_offset_backs
}


possible_side_types = ('LT', 'RT', 'Attached', 'Receiver', 'Back', 'TE','Opposite Attached and Receiver', 'Field', 'Boundary')
possible_bool = ('True', 'False')

formation_function_info = {
    'formation_structure': ('string', (), (possible_side_types,)),
    'num_receivers': ('number', ('string', 'string'), (possible_side_types, possible_bool)),
    'num_backs': ('number', (), ()),
    'num_attached': ('number', ('string', 'string'), (possible_side_types, possible_bool)),
    'num_detached': ('number', ('string', 'string'), (possible_side_types, possible_bool)),
    'surface': ('string', ('string', 'string'), (possible_side_types, possible_bool)),
    'ball_on_hash': ('bool', (), ()),
    'ball_in_middle': ('bool', (), ()),
    'ball': ('string', (), ()),
    'is_there_te': ('bool', ('string', 'string'), (possible_side_types, possible_bool)),
    'num_offset_backs': ('number', ('string', 'string'), (possible_side_types, possible_bool))
}