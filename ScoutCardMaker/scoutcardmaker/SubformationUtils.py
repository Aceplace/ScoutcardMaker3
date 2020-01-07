ATTACH_DISTANCE = 6
GHOST_DISTANCE = 4


def players_ordered(players, direction):
    if direction == 'right_to_left':
        players.sort(key=lambda player: (-player.x, player.y))
    else:
        players.sort(key=lambda player: (player.x, player.y))
    return players


def get_offense_players_ordered(subformation, direction='right_to_left'):
    players = list(subformation.players.values())
    return players_ordered(players, direction)


def get_los_players_ordered(subformation, direction='right_to_left'):
    players = list(subformation.players.values())
    players = list(filter(lambda player: player.y == 1, players))
    return players_ordered(players, direction)


def get_center(subformation):
    players = list(subformation.players.values())
    players = list(filter(lambda player: player.tag == 'C', players))
    return players[0]


def get_line_ordered(subformation, direction='right_to_left'):
    players = list(subformation.players.values())
    players = list(filter(lambda player: player.tag in ['L1', 'L2', 'L3', 'L4', 'C'], players))
    return players_ordered(players, direction)


def get_backfield_ordered(subformation, direction='right_to_left'):
    players = list(subformation.players.values())
    los_players = get_los_players_ordered(subformation, direction)
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


def get_skill_ordered(subformation, direction='right_to_left'):
    players = list(subformation.players.values())
    players = list(filter(lambda player: player.tag in ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'], players))
    return players_ordered(players, direction)


def get_attached_skill(subformation, direction='right_to_left'):
    players = list(subformation.players.values())
    core_boundaries = get_attached_boundary(players)
    skill_players = list(filter(lambda player: player.tag in ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'], players))
    skill_players_in_backfield = get_backfield_ordered(subformation)
    possibly_attached_skill = list(filter(lambda player: player not in skill_players_in_backfield, skill_players))
    attached_players = list(filter(lambda player: player.x >= core_boundaries[0] and player.x <= core_boundaries[1], possibly_attached_skill))

    return players_ordered(attached_players, direction)

def get_detached_skill(subformation, direction='right_to_left'):
    players = list(subformation.players.values())
    core_boundaries = get_attached_boundary(players)
    skill_players = list(filter(lambda player: player.tag in ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'], players))
    skill_players_in_backfield = get_backfield_ordered(subformation)
    possibly_detached_skill = list(filter(lambda player: player not in skill_players_in_backfield, skill_players))
    attached_players = list(filter(lambda player: player.x <= core_boundaries[0] or player.x >= core_boundaries[1], possibly_detached_skill))

    return players_ordered(attached_players, direction)


def get_attached_boundary(players):
    center = get_center(subformation)
    core_left = center.x - ATTACH_DISTANCE
    core_right = center.x + ATTACH_DISTANCE
    for i in range(11):
        for player in players:
            if player.x >= core_left - ATTACH_DISTANCE and player.x <= core_right + ATTACH_DISTANCE and player.y < 3:
                core_left = min(core_left, player.x - ATTACH_DISTANCE)
                core_right = max(core_right, player.x + ATTACH_DISTANCE)
    return core_left, core_right




if __name__ == '__main__':
    from Offense import Formation
    formation = Formation()
    subformation = formation.subformations['RH_LT']
    subformation.players['S6'].x = 2

    # print(get_offense_players_ordered(subformation))
    # print(get_offense_players_ordered(subformation, 'left_to_right'))
    # print(get_los_players_ordered(subformation))
    # print(get_los_players_ordered(subformation, 'left_to_right'))
    # print(get_center(subformation))
    # print(get_line_ordered(subformation))
    # print(get_backfield_ordered(subformation))
    # print(get_backfield_ordered(subformation, 'left_to_right'))
    # print(get_skill_ordered(subformation, 'left_to_right'))
    print(get_attached_skill(subformation))
    print(get_detached_skill(subformation))


# def get_align_side(direction, align_type, formation):
#     if direction == 'LT' or direction == 'RT':
#         return direction
#
#     if align_type == 'Attached':
#         strength_direction = get_attached_strength(formation)
#     elif align_type == 'Receiver':
#         strength_direction = get_receiver_strength(formation)
#     elif align_type == 'Back':
#         strength_direction = get_back_strength(formation)
#     elif align_type == 'Opposite of Attached':
#         strength_direction = get_opposite_attached_strength(formation)
#     elif align_type == 'Opposite of Receiver':
#         strength_direction = get_opposite_receiver_strength(formation)
#     elif align_type == 'Opposite Attached -> Opposite Receiver':
#         strength_direction = get_opposite_attached_and_receiver_strength(formation)
#     else: #Opposite of back strength
#         strength_direction = get_opposite_back_strength(formation)
#
#     if strength_direction == 'LT':
#         if direction == 'Str':
#             return 'LT'
#         else:
#             return 'RT'
#     else:
#         if direction == 'Str':
#             return 'RT'
#         else:
#             return 'LT'
#
# def get_direction_with_most_receivers(formation):
#     receivers_to_left_of_lt = [player for tag, player in formation.players.items() if player.x < formation.lt.x]
#     receivers_to_right_of_rt = [player for tag, player in formation.players.items() if player.x > formation.rt.x]
#
#     if len(receivers_to_left_of_lt) > len(receivers_to_right_of_rt):
#         return 'LT'
#     if len(receivers_to_left_of_lt) < len(receivers_to_right_of_rt):
#         return 'RT'
#     return None
#
# def get_direction_with_most_detached_receivers(formation):
#     attached_receivers_to_left = get_number_of_attached_receivers(formation, 'LT')
#     attached_receivers_to_right = get_number_of_attached_receivers(formation, 'RT')
#
#     if attached_receivers_to_left < attached_receivers_to_right:
#         return 'LT'
#     if attached_receivers_to_left > attached_receivers_to_right:
#         return 'RT'
#     return None
#
# def get_direction_with_most_offset_backs(formation):
#     offset_backs_to_left = get_number_of_offset_backs(formation, 'LT')
#     offset_back_to_right = get_number_of_offset_backs(formation, 'RT')
#
#     if offset_backs_to_left > offset_back_to_right:
#         return 'LT'
#     if offset_backs_to_left < offset_back_to_right:
#         return 'RT'
#     return None
#
# def get_back_strength(formation, default_strength='RT'):
#     direction = get_direction_with_most_offset_backs(formation)
#     if direction is None:
#         return get_receiver_strength(formation, default_strength)
#     return direction
#
# def get_opposite_back_strength(formation, default_strength='RT'):
#     direction = get_direction_with_most_offset_backs(formation)
#     if direction == 'LT':
#         return 'RT'
#     elif direction == 'RT':
#         return 'LT'
#     else:
#         return get_receiver_strength(formation, default_strength)
#
# def get_receiver_strength(formation, default_strength='RT'):
#
#     direction = get_direction_with_most_receivers(formation)
#     if direction:
#         return direction
#
#     if formation.hash == 'lt':
#         return 'RT'
#     elif formation.hash == 'rt':
#         return 'LT'
#
#     direction = get_direction_with_most_detached_receivers(formation)
#     if direction:
#         return direction
#
#     direction = get_direction_with_most_offset_backs(formation)
#     if direction:
#         return direction
#
#     return default_strength
#
# def get_opposite_receiver_strength(formation, default_strength='RT'):
#     receiver_strength_direction = get_receiver_strength(formation, default_strength)
#
#     if receiver_strength_direction == 'LT':
#         return 'RT'
#     else:
#         return 'LT'
#
# def get_attached_strength(formation, default_strength='RT'):
#     attached_receivers_to_left = get_number_of_attached_receivers(formation, 'LT')
#     attached_receivers_to_right = get_number_of_attached_receivers(formation, 'RT')
#
#     if attached_receivers_to_left > attached_receivers_to_right:
#         return 'LT'
#     if attached_receivers_to_left < attached_receivers_to_right:
#         return 'RT'
#
#     return get_receiver_strength(formation, default_strength)
#
# def get_opposite_attached_strength(formation, default_strength='RT'):
#     attached_receivers_to_left = get_number_of_attached_receivers(formation, 'LT')
#     attached_receivers_to_right = get_number_of_attached_receivers(formation, 'RT')
#
#     if attached_receivers_to_left > attached_receivers_to_right:
#         return 'RT'
#     if attached_receivers_to_left < attached_receivers_to_right:
#         return 'LT'
#
#     return get_receiver_strength(formation, default_strength)
#
# def get_opposite_attached_and_receiver_strength(formation, default_strength='RT'):
#     attached_receivers_to_left = get_number_of_attached_receivers(formation, 'LT')
#     attached_receivers_to_right = get_number_of_attached_receivers(formation, 'RT')
#
#     if attached_receivers_to_left > attached_receivers_to_right:
#         return 'RT'
#     if attached_receivers_to_left < attached_receivers_to_right:
#         return 'LT'
#
#     return get_opposite_receiver_strength(formation, default_strength)
#
# def get_number_of_receivers(formation, direction):
#     if direction == 'LT':
#         return len([player for tag, player in formation.players.items() if player.x < formation.lt.x])
#     elif direction == 'RT':
#         return len([player for tag, player in formation.players.items() if player.x > formation.rt.x])
#
# def get_number_of_attached_receivers(formation, direction):
#     number_of_attached_receivers = 0
#
#     if direction == 'LT':
#         sorted_receivers_outside_tackle = list(sorted([player for tag, player in formation.players.items() if player.x < formation.lt.x], key=lambda player: player.x))
#         sorted_receivers_outside_tackle.reverse()
#         outside_most_attached_player = formation.lt
#     else:
#         sorted_receivers_outside_tackle = list(sorted([player for tag, player in formation.players.items() if player.x > formation.rt.x], key=lambda player: player.x))
#         outside_most_attached_player = formation.rt
#
#     for player in sorted_receivers_outside_tackle:
#         if abs(player.x - outside_most_attached_player.x) <= ATTACH_DISTANCE:
#             number_of_attached_receivers += 1
#             outside_most_attached_player = player
#
#     return number_of_attached_receivers
#
#
# def get_number_of_offset_backs(formation, direction):
#     number_of_attached_receivers = 0
#     if direction == 'LT':
#         return len([player for tag, player in formation.players.items() if player.x >= formation.lt.x and player.x < formation.c.x])
#     else:
#         return len([player for tag, player in formation.players.items() if player.x <= formation.rt.x and player.x > formation.c.x])
#
#
# def get_first_attached(formation, direction):
#     if direction == 'LT':
#         sorted_receivers_outside_tackle = list(
#             sorted([player for tag, player in formation.players.items() if player.x < formation.lt.x],
#                    key=lambda player: player.x))
#         sorted_receivers_outside_tackle.reverse()
#         outside_most_attached_player = formation.lt
#     else:
#         sorted_receivers_outside_tackle = list(
#             sorted([player for tag, player in formation.players.items() if player.x > formation.rt.x],
#                    key=lambda player: player.x))
#         outside_most_attached_player = formation.rt
#
#     for player in sorted_receivers_outside_tackle:
#         if abs(player.x - outside_most_attached_player.x) <= ATTACH_DISTANCE:
#             return player
#
#     return None
#
#
# def get_second_attached(formation, direction):
#     number_of_attached_receivers = 0
#
#     if direction == 'LT':
#         sorted_receivers_outside_tackle = list(
#             sorted([player for tag, player in formation.players.items() if player.x < formation.lt.x],
#                    key=lambda player: player.x))
#         sorted_receivers_outside_tackle.reverse()
#         outside_most_attached_player = formation.lt
#     else:
#         sorted_receivers_outside_tackle = list(
#             sorted([player for tag, player in formation.players.items() if player.x > formation.rt.x],
#                    key=lambda player: player.x))
#         outside_most_attached_player = formation.rt
#
#     for player in sorted_receivers_outside_tackle:
#         if abs(player.x - outside_most_attached_player.x) <= ATTACH_DISTANCE:
#             number_of_attached_receivers += 1
#             if (number_of_attached_receivers == 2):
#                 return player
#             outside_most_attached_player = player
#
#     return None
#
#
# def get_receivers_outside_across(formation, direction):
#     if formation.q.x != 0:
#         receivers = [player for tag, player in formation.players.items() if tag in ['t', 'h', 'x', 'y', 'z', 'q']]
#     else:
#         receivers = [player for tag, player in formation.players.items() if tag in ['t', 'h', 'x', 'y', 'z']]
#
#     if direction == 'LT':
#         receivers.sort(key = lambda player: (player.x, player.y))
#     else:
#         receivers.sort(key = lambda player: (-1 * player.x, player.y))
#
#     return receivers
#
# def get_receivers_outside_in(formation, direction):
#     if formation.q.x != 0:
#         receivers = [player for tag, player in formation.players.items() if tag in ['t', 'h', 'x', 'y', 'z', 'q']]
#     else:
#         receivers = [player for tag, player in formation.players.items() if tag in ['t', 'h', 'x', 'y', 'z']]
#
#     if direction == 'LT':
#         receivers.sort(key = lambda player: (player.x, player.y))
#         filtered_receivers = [receiver for receiver in receivers if receiver.x < formation.lt.x]
#     else:
#         receivers.sort(key = lambda player: (-1 * player.x, player.y))
#         filtered_receivers = [receiver for receiver in receivers if receiver.x > formation.rt.x]
#
#     return filtered_receivers
#
# def get_receivers_inside_out(formation, direction):
#     if formation.q.x != 0:
#         receivers = [player for tag, player in formation.players.items() if tag in ['t', 'h', 'x', 'y', 'z', 'q']]
#     else:
#         receivers = [player for tag, player in formation.players.items() if tag in ['t', 'h', 'x', 'y', 'z']]
#
#     if direction == 'LT':
#         receivers.sort(key = lambda player: (-1 * player.x, player.y))
#         filtered_receivers = [receiver for receiver in receivers if receiver.x < formation.lt.x]
#     else:
#         receivers.sort(key = lambda player: (player.x, player.y))
#         filtered_receivers = [receiver for receiver in receivers if receiver.x > formation.rt.x]
#
#     return filtered_receivers
#
#
# def get_formation_structure(formation):
#     receivers_to_left = get_number_of_receivers(formation, 'LT')
#     receivers_to_right = get_number_of_receivers(formation, 'RT')
#     if receivers_to_left == 1 and receivers_to_right == 1:
#         return '1x1'
#     if (receivers_to_left == 1 and receivers_to_right == 2) or (receivers_to_left == 2 and receivers_to_right == 1):
#         return '2x1'
#     if receivers_to_left == 2 and receivers_to_right == 2:
#         return '2x2'
#     if (receivers_to_left == 3 and receivers_to_right == 1) or (receivers_to_left == 1 and receivers_to_right == 3):
#         return '3x1'
#     if (receivers_to_left == 3 and receivers_to_right == 2) or (receivers_to_left == 2 and receivers_to_right == 3):
#         return '3x2'
#     return '4x1'
#
#
#
# def get_surface_structures(formation, direction):
#     surface_structure = []
#     number_of_receivers = get_number_of_receivers(formation, direction)
#     number_of_attached_receivers = get_number_of_attached_receivers(formation, direction)
#     if number_of_receivers == 0:
#         surface_structure.append('Zero Receivers')
#     elif number_of_receivers == 1:
#         surface_structure.append('One Receiver')
#         surface_structure.append('At least One Receiver')
#     elif number_of_receivers == 2:
#         surface_structure.append('Two Receivers')
#         surface_structure.append('At least One Receiver')
#         surface_structure.append('At least Two Receivers')
#     elif number_of_receivers == 3:
#         surface_structure.append('Three Receivers')
#         surface_structure.append('At least One Receiver')
#         surface_structure.append('At least Two Receivers')
#         surface_structure.append('At least Three Receivers')
#     elif number_of_receivers == 4:
#         surface_structure.append('Four Receivers')
#         surface_structure.append('At least One Receiver')
#         surface_structure.append('At least Two Receivers')
#         surface_structure.append('At least Three Receivers')
#         surface_structure.append('At least Four Receivers')
#     elif number_of_receivers == 5:
#         surface_structure.append('Five Receivers')
#         surface_structure.append('At least One Receiver')
#         surface_structure.append('At least Two Receivers')
#         surface_structure.append('At least Three Receivers')
#         surface_structure.append('At least Four Receivers')
#
#     if number_of_attached_receivers == 0:
#         surface_structure.append('Zero Attached')
#     elif number_of_attached_receivers == 1:
#         surface_structure.append('One Attached')
#         surface_structure.append('At least One Attached')
#     elif number_of_attached_receivers == 2:
#         surface_structure.append('Two Attached')
#         surface_structure.append('At least One Attached')
#         surface_structure.append('At least Two Attached')
#     elif number_of_attached_receivers == 3:
#         surface_structure.append('Three Attached')
#         surface_structure.append('At least One Attached')
#         surface_structure.append('At least Two Attached')
#         surface_structure.append('At least Three Attached')
#     elif number_of_attached_receivers == 4:
#         surface_structure.append('Four Attached')
#         surface_structure.append('At least One Attached')
#         surface_structure.append('At least Two Attached')
#         surface_structure.append('At least Three Attached')
#         surface_structure.append('At least Four Attached')
#     elif number_of_attached_receivers == 5:
#         surface_structure.append('Five Attached')
#         surface_structure.append('At least One Attached')
#         surface_structure.append('At least Two Attached')
#         surface_structure.append('At least Three Attached')
#         surface_structure.append('At least Four Attached')
#
#
#     if number_of_receivers == 1 and number_of_attached_receivers == 1:
#         surface_structure.append('Nub')
#     if number_of_receivers == 1 and number_of_attached_receivers == 0:
#         surface_structure.append('Split')
#
#     if number_of_receivers == 2 and number_of_attached_receivers == 0:
#         surface_structure.append('Twin')
#     if number_of_receivers == 2 and number_of_attached_receivers == 1:
#         surface_structure.append('Pro')
#     if number_of_receivers == 2 and number_of_attached_receivers == 2:
#         surface_structure.append('Wing')
#
#     if number_of_receivers == 3 and number_of_attached_receivers == 0:
#         surface_structure.append('Trips')
#     if number_of_receivers == 3 and number_of_attached_receivers == 1:
#         surface_structure.append('Indy')
#     if number_of_receivers == 3 and number_of_attached_receivers == 2:
#         surface_structure.append('Indy Wing')
#     if number_of_receivers == 3 and number_of_attached_receivers == 3:
#         surface_structure.append('Tight Bunch')
#
#     return surface_structure


