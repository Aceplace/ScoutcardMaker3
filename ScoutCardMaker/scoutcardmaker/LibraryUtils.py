class PersonnelLabelMapper:
    def __init__(self, side):
        if side == 'offense':
            self.mappings = {'L1': 'LT',
                             'L2': 'LG',
                             'L3': 'RG',
                             'L4': 'RT',
                             'C': 'C',
                             'S1': 'Q',
                             'S2': 'T',
                             'S3': 'H',
                             'S4': 'X',
                             'S5': 'Y',
                             'S6': 'Z'}
        else:
            self.mappings = {'D1': 'T',
                             'D2': 'N',
                             'D3': 'P',
                             'D4': 'A',
                             'D5': 'B',
                             'D6': 'M',
                             'D7': 'W',
                             'D8': 'S',
                             'D9': 'F',
                             'D10': 'C',
                             '11': 'Q'}

    def get_label(self, tag):
        return self.mappings[tag]

    def to_dict(self):
        return self.mappings

    def __repr__(self):
        return f'Personnel Mapper({self.mappings})'

    @staticmethod
    def from_dict(obj):
        label_mapper = PersonnelLabelMapper()
        label_mapper.mappings = obj
        return label_mapper
