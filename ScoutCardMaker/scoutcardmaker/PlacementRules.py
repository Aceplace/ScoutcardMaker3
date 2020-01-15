from Utils import INVALID_POSITION
import scoutcardmaker.SubformationUtils as su


def absolute(subformation, arguments):
    x = int(arguments[0])
    y = int(arguments[1])
    return x, y


GHOST_DISTANCE = 4


def tech_alignment(subformation, arguments):
    side_type = arguments[0]
    alignment = arguments[1]
    y = arguments[2]
    flip = bool(arguments[3])

    align_side = su.get_side(side_type, subformation.players, subformation.hash_mark)
    if flip:
        align_side = 'RT' if align_side == 'LT' else 'RT'

    offset = -1 if 'i' in alignment else 1
    offset = offset if align_side == 'RT' else offset * -1
    if alignment in ['Zero', 'Two', 'Four', 'Six', 'Eight']:
        offset = 0
    # ('0', '1', '2i', '2', '3', '3', '4i', '4', '5', '6i', '6', '7', '8i', '8', '9')
    # Get alignment player
    if alignment in ['0', '1']:
        align_player = su.get_center(subformation.players)
    elif alignment in ['2i', '2', '3']:
        align_player = su.get_lg(subformation.players) if align_side == 'LT' else su.get_rg(subformation.players)
    elif alignment in ['4i', '4', '5']:
        align_player = su.get_lt(subformation.players) if align_side == 'LT' else su.get_rt(subformation.players)
    elif alignment in ['6i', '6', '7']:
        align_player = su.get_first_attached(subformation.players, 'LT')\
            if align_side == 'LT' else su.get_first_attached(subformation.players, 'RT')
        ghost_distance_multiplier = 1
    elif alignment in ['8i', '8', '9']:
        align_player = su.get_second_attached(subformation.players, 'LT') \
            if align_side == 'LT' else su.get_second_attached(subformation.players, 'RT')
        ghost_distance_multiplier = 2

    if align_player:
        x = align_player.x + offset
    else:
        x = su.get_rt(subformation.players) + GHOST_DISTANCE * ghost_distance_multiplier \
            if align_side == 'RT' else \
            su.get_lt(subformation.players) - GHOST_DISTANCE * ghost_distance_multiplier

    return x, y


def over(subformation, arguments):
    side_type = arguments[0]
    over = arguments[1]
    y = arguments[2]
    offset = arguments[3]
    flip = bool(arguments[4])

    align_side = su.get_side(side_type, subformation.players, subformation.hash_mark)
    if flip:
        align_side = 'RT' if align_side == 'LT' else 'RT'
    receivers_outside_across = su.get_skill_ordered(subformation.players,
                                                    'right_to_left' if align_side == 'RT' else 'left_to_right')
    offset = offset if align_side == 'RT' else -offset

    if over == '#1':
        x = receivers_outside_across[0].x + offset
    elif over == '#2':
        x = receivers_outside_across[1].x + offset
    elif over == '#3':
        x = receivers_outside_across[2].x + offset
    elif over == '#4':
        x = receivers_outside_across[3].x + offset

    return x, y


def apex(subformation, arguments):
    side_type = arguments[0]
    apex_type = arguments[1]
    y = arguments[2]
    flip = arguments[3]

    align_side = su.get_side(side_type, subformation.players, subformation.hash_mark)
    if flip:
        align_side = 'RT' if align_side == 'LT' else 'RT'
    receivers_inside_out = su.get_receivers_inside_out(subformation.players, 'LT') if align_side == 'LT' \
        else su.get_receivers_inside_out(subformation.players, 'RT')
    receivers_outside_in = su.get_receivers_outside_in(subformation.players, 'LT') if align_side == 'LT' \
        else su.get_receivers_outside_in(subformation.players, 'RT')

    if apex_type == 'T_1st':
        if len(receivers_inside_out) >= 1:
            x = (receivers_inside_out[0].x + su.get_lt(subformation.players)) // 2 if align_side == 'LT' \
                else (receivers_inside_out[0].x + su.get_rt(subformation.players)) // 2
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


placement_rules = {
    'absolute': absolute,
    'tech_alignment': tech_alignment,
    'over': over,
    'apex': apex
}

possible_side_types = ('LT', 'RT', 'Attached', 'Receiver', 'Back', 'Opposite Attached and Receiver', 'Field', 'Boundary')
possible_alignments = ('0', '1', '2i', '2', '3', '4i', '4', '5', '6i', '6', '7', '8i', '8', '9')
possible_overs = ('#1', '#2', '#3', '#4')
possible_apex = ('T_1st', '3_2', '2_1')
possible_bool = ('True', 'False')

placement_rule_info = {
    'absolute': (('int', 'int'), ((), ())),
    'tech_alignment': (('string', 'string', 'int', 'string'), (possible_side_types, possible_alignments, (), possible_bool)),
    'over': (('string', 'string', 'int', 'int', 'string'), (possible_side_types, possible_overs, (), (), possible_bool)),
    'apex': (('string', 'string', 'int', 'string'), (possible_side_types, possible_apex, (), possible_bool))
}