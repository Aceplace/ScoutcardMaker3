ATTACH_DISTANCE = 6
GHOST_DISTANCE = 4

def opposite_direction(direction):
    assert direction in ['LT', 'RT']
    if direction == 'RT':
        return 'LT'
    return 'RT'

def players_ordered(players, direction):
    assert direction in ['right_to_left', 'left_to_right']
    if direction == 'right_to_left':
        players.sort(key=lambda player: (-player.x, player.y))
    else:
        players.sort(key=lambda player: (player.x, player.y))
    return players


def players_on_side(center_x, players, direction):
    assert direction in ['RT', 'LT']
    if direction == 'RT':
        return [player for player in players if player.x > center_x]
    else:
        return [player for player in players if player.x < center_x]


def distance_from_center(center_x, player):
    return abs(center_x - player.x)


def get_offense_players_ordered(players, direction='right_to_left'):
    return players_ordered(players, direction)


def get_los_players_ordered(players, direction='right_to_left'):
    players = list(filter(lambda player: player.y == 1, players))
    return players_ordered(players, direction)


def get_center(players):
    players = list(filter(lambda player: player.tag == 'C', players))
    return players[0]


def get_line_ordered(players, direction='right_to_left'):
    players = list(filter(lambda player: player.tag in ['L1', 'L2', 'L3', 'L4', 'C'], players))
    return players_ordered(players, direction)


def get_backfield_ordered(players, direction='right_to_left'):
    los_players = get_los_players_ordered(players, direction)
    center_index = 0
    for index, player in enumerate(los_players):
        if player.tag == 'C':
            center_index = index
            break
    tackle1_x, tackle2_x = los_players[center_index + 2].x, los_players[center_index - 2].x
    left_backfield_boundary = min(tackle1_x, tackle2_x)
    right_backfield_boundary = max(tackle1_x, tackle2_x)
    players = list(filter(lambda player: player.y > 1 and player.x >= left_backfield_boundary and player.x <= right_backfield_boundary,
                          players))
    return players_ordered(players, direction)


def get_skill_ordered(players, direction='right_to_left'):
    players = list(filter(lambda player: player.tag in ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'], players))
    return players_ordered(players, direction)


def get_attached_skill_ordered(players, direction='right_to_left'):
    core_boundaries = get_attached_boundary(players)
    skill_players = list(filter(lambda player: player.tag in ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'], players))
    skill_players_in_backfield = get_backfield_ordered(players)
    possibly_attached_skill = list(filter(lambda player: player not in skill_players_in_backfield, skill_players))
    attached_players = list(filter(lambda player: player.x >= core_boundaries[0] and player.x <= core_boundaries[1], possibly_attached_skill))

    return players_ordered(attached_players, direction)


def get_tightends_ordered(players, direction='right_to_left'):
    attached_players = get_attached_skill_ordered(players, 'right_to_left')
    center = get_center(players)
    players_to_right = players_on_side(center.x, attached_players, 'RT')
    players_to_left = players_on_side(center.x, attached_players, 'LT')

    tightends = []
    if len(players_to_right) > 0 and players_to_right[-1].y == 1:
        tightends.append(players_to_right[-1])
    if len(players_to_left) > 0 and players_to_left[0].y == 1:
        tightends.append(players_to_left[0])

    return players_ordered(tightends, direction)

def get_all_oline(players):
    players_ordered = get_los_players_ordered(players, 'right_to_left')
    center_index = -1
    for i in range(len(players_ordered)):
        if players_ordered[i].tag == 'C':
            center_index = i
            break
    return players_ordered[i + 2], players_ordered[i + 1], players_ordered[i - 1], players_ordered[i -2]


def get_lt(players):
    return get_all_oline(players)[0]


def get_lg(players):
    return get_all_oline(players)[1]


def get_rg(players):
    return get_all_oline(players)[2]


def get_rt(players):
    return get_all_oline(players)[3]


def get_detached_skill_ordered(players, direction='right_to_left'):
    core_boundaries = get_attached_boundary(players)
    skill_players = list(filter(lambda player: player.tag in ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'], players))
    skill_players_in_backfield = get_backfield_ordered(players)
    possibly_detached_skill = list(filter(lambda player: player not in skill_players_in_backfield, skill_players))
    attached_players = list(filter(lambda player: player.x <= core_boundaries[0] or player.x >= core_boundaries[1], possibly_detached_skill))

    return players_ordered(attached_players, direction)

def get_receivers_ordered(players, direction='right_to_left'):
    attached = get_attached_skill_ordered(players)
    detached = get_detached_skill_ordered(players)
    receivers = attached + detached

    return players_ordered(receivers, direction)


def get_attached_boundary(players):
    center = get_center(players)
    core_left = center.x - ATTACH_DISTANCE
    core_right = center.x + ATTACH_DISTANCE
    for i in range(11):
        for player in players:
            if player.x >= core_left - ATTACH_DISTANCE and player.x <= core_right + ATTACH_DISTANCE and player.y < 3:
                core_left = min(core_left, player.x - ATTACH_DISTANCE)
                core_right = max(core_right, player.x + ATTACH_DISTANCE)
    return core_left, core_right


def get_direction_with_most_receivers(players):
    receivers_to_left_of_lt = [player for player in players if player.x < get_lt(players).x]
    receivers_to_right_of_rt = [player for player in players if player.x > get_rt(players).x]

    if len(receivers_to_left_of_lt) > len(receivers_to_right_of_rt):
        return 'LT'
    if len(receivers_to_left_of_lt) < len(receivers_to_right_of_rt):
        return 'RT'
    return None


def get_num_offset_backs(players, direction):
    center_x = get_center(players)
    backs = get_backfield_ordered(players)
    return len(players_on_side(center_x, backs, direction))


def get_num_receivers(players, direction):
    center_x = get_center(players)
    receivers = get_receivers_ordered(players)
    return len(players_on_side(center_x, receivers, direction))


def get_num_attached(players, direction):
    center_x = get_center(players)
    attached = get_attached_skill_ordered(players)
    return len(players_on_side(center_x, attached, direction))


def get_num_detached(players, direction):
    center_x = get_center(players)
    detached = get_attached_skill_ordered(players)
    return len(players_on_side(center_x, detached, direction))


def get_direction_with_most_attached_receivers(players):
    attached_receivers = get_attached_skill_ordered(players)
    center_x = get_center(players).x
    attached_receivers_to_left = players_on_side(center_x, attached_receivers, 'LT')
    attached_receivers_to_right = players_on_side(center_x, attached_receivers, 'RT')

    if attached_receivers_to_left > attached_receivers_to_right:
        return 'LT'
    if attached_receivers_to_left < attached_receivers_to_right:
        return 'RT'
    return None


def get_direction_with_most_detached_receivers(players):
    detached_receivers = get_detached_skill_ordered(players)
    center_x = get_center(players).x
    detached_receivers_to_left = players_on_side(center_x, detached_receivers, 'LT')
    detached_receivers_to_right = players_on_side(center_x, detached_receivers, 'RT')

    if detached_receivers_to_left > detached_receivers_to_right:
        return 'LT'
    if detached_receivers_to_left < detached_receivers_to_right:
        return 'RT'
    return None


def get_direction_with_most_offset_backs(players):
    backs = get_backfield_ordered(players)
    center_x = get_center(players).x
    offset_backs_to_left = players_on_side(center_x, backs, 'LT')
    offset_back_to_right = players_on_side(center_x, backs, 'RT')

    if offset_backs_to_left > offset_back_to_right:
        return 'LT'
    if offset_backs_to_left < offset_back_to_right:
        return 'RT'
    return None


def get_receiver_strength(players, hash, default_strength='RT'):
    direction = get_direction_with_most_receivers(players)
    if direction:
        return direction

    if hash == 'LT':
        return 'RT'
    elif hash == 'RT':
        return 'LT'

    direction = get_direction_with_most_detached_receivers(formation)
    if direction:
        return direction

    return default_strength


def get_back_strength(players, hash, default_strength='RT'):
    direction = get_direction_with_most_offset_backs(players)
    if direction is None:
        return get_receiver_strength(players, hash, default_strength)
    return direction


def get_attached_strength(players, hash, default_strength='RT'):
    direction = get_direction_with_most_attached_receivers(players)
    if direction is None:
        return get_receiver_strength(players, hash, default_strength)
    return direction


def get_opposite_attached_and_receiver_strength(players, hash, default_strength='RT'):
    attached_receivers_to_left = get_num_attached(players, 'LT')
    attached_receivers_to_right = get_num_attached(players, 'RT')

    if attached_receivers_to_left > attached_receivers_to_right:
        return 'RT'
    if attached_receivers_to_left < attached_receivers_to_right:
        return 'LT'

    return opposite_direction(get_receiver_strength(players, hash, default_strength))


def get_receivers_outside_in(players, direction):
    center_x = get_center(players).x
    receivers = get_receivers_ordered(players)
    if direction == 'RT':
        return players_ordered(players_on_side(center_x, receivers, direction), 'right_to_left')
    else:
        return players_ordered(players_on_side(center_x, receivers, direction), 'left_to_right')


def get_receivers_inside_out(players, direction):
    center_x = get_center(players).x
    receivers = get_receivers_ordered(players)
    if direction == 'RT':
        return players_ordered(players_on_side(center_x, receivers, direction), 'left_to_right')
    else:
        return players_ordered(players_on_side(center_x, receivers, direction), 'right_to_left')


def get_first_attached(players, direction):
    center_x = get_center(players).x
    attached_players_to_side = players_on_side(center_x, get_attached_skill_ordered(players), direction)
    if len(attached_players_to_side) > 0:
        return players_ordered(attached_players_to_side, 'left_to_right' if direction == 'RT' else 'right_to_left')[0]
    return None


def get_second_attached(players, direction):
    center_x = get_center(players).x
    attached_players_to_side = players_on_side(center_x, get_attached_skill_ordered(players), direction)
    if len(attached_players_to_side) > 1:
        return players_ordered(attached_players_to_side, 'left_to_right' if direction == 'RT' else 'right_to_left')[1]
    return None


def get_third_attached(players, direction):
    center_x = get_center(players).x
    attached_players_to_side = players_on_side(center_x, get_attached_skill_ordered(players), direction)
    if len(attached_players_to_side) > 2:
        return players_ordered(attached_players_to_side, 'left_to_right' if direction == 'RT' else 'right_to_left')[2]
    return None


def get_align_side(align_type, players, hash):
    if align_type == 'LT' or align_type == 'RT':
        return align_type

    if align_type == 'Attached':
        return get_attached_strength(players, hash)
    elif align_type == 'Receiver':
        return get_receiver_strength(players, hash)
    elif align_type == 'Back':
        return get_back_strength(players, hash)
    elif align_type == 'Opposite Attached and Receiver':
        return get_opposite_attached_and_receiver_strength(players, hash)
    elif align_type == 'Field':
        if hash == 'RT':
            return 'LT'
        else:
            return 'RT'
    else: # align_type == 'Boundary'
        if hash == 'LT':
            return 'LT'
        else:
            return 'RT'


def get_formation_structure(players):
    receivers_to_left = get_num_receivers(players, 'LT')
    receivers_to_right = get_num_receivers(players, 'RT')
    if receivers_to_left == 1 and receivers_to_right == 1:
        return '1x1'
    if (receivers_to_left == 1 and receivers_to_right == 2) or (receivers_to_left == 2 and receivers_to_right == 1):
        return '2x1'
    if receivers_to_left == 2 and receivers_to_right == 2:
        return '2x2'
    if (receivers_to_left == 3 and receivers_to_right == 1) or (receivers_to_left == 1 and receivers_to_right == 3):
        return '3x1'
    if (receivers_to_left == 3 and receivers_to_right == 2) or (receivers_to_left == 2 and receivers_to_right == 3):
        return '3x2'
    return '4x1'


if __name__ == '__main__':
    from Offense import Formation
    formation = Formation()
    subformation = formation.subformations['RH_LT']
    subformation.players['S6'].x = 2
    players = list(subformation.players.values())

    print(get_offense_players_ordered(players))
    print(get_offense_players_ordered(players, 'left_to_right'))
    print(get_los_players_ordered(players))
    print(get_los_players_ordered(players, 'left_to_right'))
    print(get_center(players))
    print(get_line_ordered(players))
    print(get_backfield_ordered(players))
    print(get_backfield_ordered(players, 'left_to_right'))
    print(get_skill_ordered(players, 'left_to_right'))
    print(get_attached_skill_ordered(players))
    print(get_detached_skill_ordered(players))
    print(get_tightends_ordered(players, 'left_to_right'))



