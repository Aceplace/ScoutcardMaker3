import json

with open('library.json') as file:
    library = json.load(file)

for formation in library['formations'].values():
    for key, subformation in formation['subformations'].items():
        if key in ['MOF_RT', 'MOF_LT']:
            subformation['hash'] = 'MOF'
        if key in ['LH_RT', 'LH_LT']:
            subformation['hash'] = 'LT'
        if key in ['RH_RT', 'RH_LT']:
            subformation['hash'] = 'RT'

with open('library2.json', 'w') as file:
    json.dump(library, file, indent=4)
