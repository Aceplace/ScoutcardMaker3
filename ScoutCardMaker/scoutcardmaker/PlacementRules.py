from scoutcardmaker.Utils import INVALID_POSITION
import scoutcardmaker.SubformationUtils as sutils

# TODO(aceplace): Figure out how we will do unbalanced

def absolute(subformation, defense, arguments, optional_arguments):
    x = int(arguments[0])
    y = int(arguments[1])
    return x, y


GHOST_DISTANCE = 4


def tech_alignment(subformation, defense, arguments, optional_arguments):
    side_type = arguments[0]
    alignment = arguments[1]
    y = int(arguments[2])
    flip = True if arguments[3] == 'True' else False

    players_list = list(subformation.players.values())

    align_side = sutils.get_side(side_type, players_list, subformation.hash_mark)
    if flip:
        align_side = 'RT' if align_side == 'LT' else 'LT'

    offset = -1 if 'i' in alignment else 1
    offset = offset if align_side == 'RT' else offset * -1
    if alignment in ['0', '2', '4', '6', '8']:
        offset = 0
    # Get alignment player
    if alignment in ['0', '1']:
        align_player = sutils.get_center(players_list)
    elif alignment in ['2i', '2', '3']:
        align_player = sutils.get_lg(players_list) if align_side == 'LT' else sutils.get_rg(players_list)
    elif alignment in ['4i', '4', '5']:
        align_player = sutils.get_lt(players_list) if align_side == 'LT' else sutils.get_rt(players_list)
    elif alignment in ['6i', '6', '7']:
        align_player = sutils.get_first_attached(players_list, 'LT')\
            if align_side == 'LT' else sutils.get_first_attached(players_list, 'RT')
        ghost_distance_multiplier = 1
    elif alignment in ['8i', '8', '9']:
        align_player = sutils.get_second_attached(players_list, 'LT') \
            if align_side == 'LT' else sutils.get_second_attached(players_list, 'RT')
        ghost_distance_multiplier = 2

    if align_player:
        x = align_player.x + offset
    else:
        x = sutils.get_rt(players_list).x + GHOST_DISTANCE * ghost_distance_multiplier \
            if align_side == 'RT' else \
            sutils.get_lt(players_list).x - GHOST_DISTANCE * ghost_distance_multiplier

    if 'slide_in_if_covered' in optional_arguments:
        min_x, max_x = (x - 5, x + 1) if align_side == 'LT' else (x - 1, x + 5)
        if is_a_defender_between(defense, min_x, max_x, 1):
            x = x + 3 if align_side == 'LT' else x - 3

    return x, y


def over(subformation, defense, arguments, optional_arguments):
    side_type = arguments[0]
    over = arguments[1]
    y = int(arguments[2])
    offset = int(arguments[3])
    flip = True if arguments[4] == 'True' else False

    players_list = list(subformation.players.values())

    align_side = sutils.get_side(side_type, players_list, subformation.hash_mark)
    if flip:
        align_side = 'RT' if align_side == 'LT' else 'LT'

    player_direction_outside_accross = 'right_to_left' if align_side == 'RT' else 'left_to_right'
    receivers_outside_across = sutils.get_skill_ordered(players_list, player_direction_outside_accross)

    offset = offset if align_side == 'RT' else -offset

    player_defender_is_over = None
    if over == '#1':
        player_defender_is_over = receivers_outside_across[0]
    elif over == '#2':
        player_defender_is_over = receivers_outside_across[1]
    elif over == '#3':
        player_defender_is_over = receivers_outside_across[2]
    elif over == '#4':
        player_defender_is_over = receivers_outside_across[3]
    elif over == 'last_attached':
        player_defender_is_over = sutils.get_outside_most_attached_or_tackle(players_list, align_side)
    elif over == 'first_attached':
        player_defender_is_over = sutils.get_first_attached(players_list, align_side)
    elif over == 'los_between_2_1':
        player_defender_is_over = receivers_outside_across[1] if receivers_outside_across[1].y == 1 else receivers_outside_across[0]
    elif over == 'non_los_between_2_1':
        player_defender_is_over = receivers_outside_across[1] if receivers_outside_across[1].y != 1 else receivers_outside_across[0]
    elif over == 'los_between_3_2':
        player_defender_is_over = receivers_outside_across[2] if receivers_outside_across[2].y == 1 else receivers_outside_across[1]
    elif over == 'non_los_between_3_2':
        player_defender_is_over = receivers_outside_across[2] if receivers_outside_across[2].y != 1 else receivers_outside_across[1]

    x = player_defender_is_over.x + offset

    if 'back_off_if_occupied' in optional_arguments:
        min_x, max_x = (player_defender_is_over.x - 5, player_defender_is_over.x + 1) if align_side == 'LT' else (player_defender_is_over.x - 1, player_defender_is_over.x + 5)
        if is_a_defender_between(defense, min_x, max_x, 3):
            y = 5

    if 'back_off_further_if_occupied' in optional_arguments:
        min_x, max_x = (player_defender_is_over.x - 5, player_defender_is_over.x + 1) if align_side == 'LT' else (player_defender_is_over.x - 1, player_defender_is_over.x + 5)
        if is_a_defender_between(defense, min_x, max_x, 3):
            y = 7

    if 'back_off_wing' in optional_arguments and y < 2 and player_defender_is_over.y > 1:
        y = 2

    return x, y


def over_unbalanced_player(subformation, defense, arguments, optional_arguments):
    y = int(arguments[0])
    offset = int(arguments[1])

    players_list = list(subformation.players.values())

    unbalanced_player = sutils.get_unbalanced_player(players_list)
    if not unbalanced_player:
        return INVALID_POSITION

    unbalanced_player_side = sutils.get_unbalanced_side(players_list)
    if unbalanced_player_side == 'LT':
        x = unbalanced_player.x - offset
    else:
        x = unbalanced_player.x + offset

    return x, y

def apex(subformation, defense, arguments, optional_arguments):
    side_type = arguments[0]
    apex_type = arguments[1]
    y = int(arguments[2])
    flip = True if arguments[3] == 'True' else False

    players_list = list(subformation.players.values())

    align_side = sutils.get_side(side_type, players_list, subformation.hash_mark)
    if flip:
        align_side = 'RT' if align_side == 'LT' else 'LT'
    receivers_inside_out = sutils.get_receivers_inside_out(players_list, 'LT') if align_side == 'LT' \
        else sutils.get_receivers_inside_out(players_list, 'RT')
    receivers_outside_in = sutils.get_receivers_outside_in(players_list, 'LT') if align_side == 'LT' \
        else sutils.get_receivers_outside_in(players_list, 'RT')

    if apex_type == 'T_1st':
        if len(receivers_inside_out) >= 1:
            x = (receivers_inside_out[0].x + sutils.get_lt(players_list).x) // 2 if align_side == 'LT' \
                else (receivers_inside_out[0].x + sutils.get_rt(players_list).x) // 2
        else:
            x, y = INVALID_POSITION
    elif apex_type == '3_2':
        if len(receivers_outside_in) >= 3:
            x = (receivers_outside_in[2].x + receivers_outside_in[1].x) // 2
        else:
            x, y = INVALID_POSITION
    else:  # apex_type == '2_1:
        if len(receivers_outside_in) >= 2:
            x = (receivers_outside_in[1].x + receivers_outside_in[0].x) // 2
        else:
            x, y = INVALID_POSITION

    return x, y

def first_open_gap(subformation, defense, arguments, optional_arguments):
    side_type = arguments[0]
    y = int(arguments[1])
    flip = True if arguments[2] == 'True' else False

    players_list = list(subformation.players.values())

    align_side = sutils.get_side(side_type, players_list, subformation.hash_mark)
    if flip:
        align_side = 'RT' if align_side == 'LT' else 'LT'

    inside_lineman_x = sutils.get_center(players_list).x
    if align_side == 'RT':
        outside_lineman_x = sutils.get_rg(players_list).x
        if not is_a_defender_between(defense, inside_lineman_x, outside_lineman_x, 5):
            return (inside_lineman_x + outside_lineman_x) // 2, y

        inside_lineman_x = outside_lineman_x
        outside_lineman_x = sutils.get_rt(players_list).x
        if not is_a_defender_between(defense, inside_lineman_x, outside_lineman_x, 5):
            return (inside_lineman_x + outside_lineman_x) // 2, y

        return outside_lineman_x + 2, y

    outside_lineman_x = sutils.get_lg(players_list).x
    if not is_a_defender_between(defense, outside_lineman_x, inside_lineman_x, 5):
        return (inside_lineman_x + outside_lineman_x) // 2, y

    inside_lineman_x = outside_lineman_x
    outside_lineman_x = sutils.get_lt(players_list).x
    if not is_a_defender_between(defense, outside_lineman_x, inside_lineman_x, 5):
        return (inside_lineman_x + outside_lineman_x) // 2, y

    return outside_lineman_x - 2, y


# todo(aceplace) : Second open gap
# todo(aceplace) : Figure out how to modify from previously placed defenders (in a composite formation)

placement_rules = {
    'absolute': absolute,
    'tech_alignment': tech_alignment,
    'over': over,
    'apex': apex,
    'first_open_gap': first_open_gap,
    'over_unbalanced_player': over_unbalanced_player,
}

possible_side_types = ('LT', 'RT', 'Attached', 'Receiver', 'Back', 'TE', 'Opposite_Attached_and_Receiver', 'Field', 'Boundary')
possible_alignments = ('0', '1', '2i', '2', '3', '4i', '4', '5', '6i', '6', '7', '8i', '8', '9')
possible_overs = ('#1', '#2', '#3', '#4', 'last_attached', 'first_attached', 'los_between_2_1', 'non_los_between_2_1', 'los_between_3_2', 'non_los_between_3_2')
possible_apex = ('T_1st', '3_2', '2_1')
possible_bool = ('True', 'False')

placement_rule_info = {
    'absolute': (('int', 'int'), ((), ())),
    'tech_alignment': (('string', 'string', 'int', 'string'), (possible_side_types, possible_alignments, (), possible_bool)),
    'over': (('string', 'string', 'int', 'int', 'string'), (possible_side_types, possible_overs, (), (), possible_bool)),
    'apex': (('string', 'string', 'int', 'string'), (possible_side_types, possible_apex, (), possible_bool)),
    'first_open_gap': (('string', 'int', 'string'), (possible_side_types, (), possible_bool)),
    'over_unbalanced_player': (('int', 'int'), ((), ())),
}

# Support methods
def is_a_defender_between(defense, x1, x2, maxy):
    affected_defenders = [defender for defender in defense.players.values() if defender.tag in defense.affected_tags]
    return any(defender.placed_x > x1 and defender.placed_x < x2 and defender.placed_y <= maxy for defender in affected_defenders)

# Optionals