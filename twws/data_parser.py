import ast
import json
import pandas as pd

DIRECTORY = '../data/'


def get_trait_list(data_list: list, trait_name: str, field_name: str) -> list:
    abilities_list = []
    for n, data in enumerate(data_list):
        if len(data[trait_name]) > 0:
            for a in data[trait_name]:
                abilities_list.append(a[field_name])
    return list(set(abilities_list))


def load_data(directory):
    with open(f'{directory}data.txt', 'r') as f:
        data_list = f.read()

    data_list = ast.literal_eval(data_list)

    with open(f'{directory}template_unit.json', 'r') as f:
        template_unit = f.read()

    template_unit = json.loads(template_unit)

    return data_list, template_unit


def parse_jsons(data_list, template_unit):
    direct_keys = []
    non_direct_keys = []

    exclude_list = ['rank', 'fatigue', 'singleplayer_cost', 'singleplayer_upkeep', 'create_time', 'category_icon',
                    'category_tooltip', 'fatigue_modifier', 'walk_speed', 'turn_speed', 'damage_mod_all']

    for key in template_unit.keys():
        if isinstance(template_unit[key], float) or isinstance(template_unit[key], int) or isinstance(
                template_unit[key], str) or isinstance(template_unit[key], bool) or template_unit[key] is None:
            if key not in exclude_list:
                direct_keys.append(key)
        else:
            non_direct_keys.append(key)

    abilities_list = get_trait_list(data_list, 'abilities', 'name')
    spells_list = get_trait_list(data_list, 'spells', 'name')
    attributes_list = get_trait_list(data_list, 'attributes', 'key')

    primary_melee_weapon_keys = list(template_unit['primary_melee_weapon'].keys())
    primary_melee_weapon_keys.remove('phase')
    primary_melee_weapon_keys.remove('tww_version')

    primary_missile_weapon_keys = list(template_unit['primary_missile_weapon'].keys())
    primary_missile_weapon_keys.remove('phase')
    primary_missile_weapon_keys.remove('projectile')
    primary_missile_weapon_keys.remove('tww_version')

    secondary_missile_weapon_keys = list(template_unit['secondary_missile_weapon'].keys())
    secondary_missile_weapon_keys.remove('phase')
    secondary_missile_weapon_keys.remove('projectile')
    secondary_missile_weapon_keys.remove('tww_version')

    df = []
    columns = direct_keys + \
              ['faction_id', 'group_name'] + \
              ['ability__' + i for i in abilities_list] + \
              ['spell__' + i for i in spells_list] + \
              ['attribute__' + i for i in attributes_list] + \
              ['melee__' + i for i in primary_melee_weapon_keys] + \
              ['melee__phase'] + \
              ['missile_primary__' + i for i in primary_missile_weapon_keys] + \
              ['missile_primary__phase'] + \
              ['missile_secondary__' + i for i in secondary_missile_weapon_keys] + \
              ['missile_secondary__phase']

    for n, data in enumerate(data_list):
        if len(data['factions']) > 0:
            row = [data[key] for key in direct_keys]
            row.append(data['factions'][0]['name_group'])
            row.append(data['ground_stat_effect_group']['group_name'])
            abbs = [i['name'] for i in data['abilities']]
            abbs_bin = [1 if i in abbs else 0 for i in abilities_list]
            row.extend(abbs_bin)

            spells = [i['name'] for i in data['spells']]
            spells_bin = [1 if i in spells else 0 for i in spells_list]
            row.extend(spells_bin)

            attributes = [i['key'] for i in data['attributes']]
            attributes_bin = [1 if i in attributes else 0 for i in attributes_list]
            row.extend(attributes_bin)

            primary_melee_weapon = [data['primary_melee_weapon'][key] for key in primary_melee_weapon_keys]
            row.extend(primary_melee_weapon)
            if data['primary_melee_weapon']['phase'] is None:
                row.append(None)
            else:
                row.append(data['primary_melee_weapon']['phase']['name'])

            primary_missile_weapon = [
                data['primary_missile_weapon'][key] if key in data['primary_missile_weapon'].keys() else None for key in
                primary_missile_weapon_keys]
            row.extend(primary_missile_weapon)
            if len(data['primary_missile_weapon'].keys()) == 0:
                row.append(None)
            elif data['primary_missile_weapon']['phase'] is None:
                row.append(None)
            else:
                row.append(data['primary_missile_weapon']['phase']['name'])

            secondary_missile_weapon = [
                data['secondary_missile_weapon'][key] if key in data['secondary_missile_weapon'].keys() else None for
                key in secondary_missile_weapon_keys]
            row.extend(secondary_missile_weapon)
            if len(data['secondary_missile_weapon'].keys()) == 0:
                row.append(None)
            elif data['secondary_missile_weapon']['phase'] is None:
                row.append(None)
            else:
                row.append(data['secondary_missile_weapon']['phase']['name'])

            df.append(row)

    df = pd.DataFrame(df, columns=columns)

    return df


if __name__ == '__main__':
    data_list, template_unit = load_data(DIRECTORY)
    df = parse_jsons(data_list, template_unit)
    df.to_csv(DIRECTORY + 'data.csv', index=False)
