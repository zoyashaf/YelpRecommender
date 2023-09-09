
import argparse
import collections
import csv
import json

def read_and_write_file(json_file_path, csv_file_path, column_names):

    with open(csv_file_path, 'w+') as fout:
        csv_file = csv.writer(fout)
        csv_file.writerow(list(column_names))
        with open(json_file_path) as fin:
            for line in fin:
                line_contents = json.loads(line)
                csv_file.writerow(get_row(line_contents, column_names))

def get_superset_of_column_names_from_file(json_file_path):
    column_names = set()
    with open(json_file_path) as fin:
        for line in fin:
            line_contents = json.loads(line)
            column_names.update(
                    set(get_column_names(line_contents).keys())
                    )
    return column_names

def get_column_names(line_contents, parent_key=''):
    
    """Flattens the key value pairs.
    Example:
        line_contents = {
                'a': {
                    'b': 2,
                    'c': 3,
                    },
        }
        will return: ['a.b', 'a.c']
    a.b and a.c are the column names for the final csv file.
    """
    column_names = []
    for k, v in line_contents.items():
        column_name = "{0}.{1}".format(parent_key, k) if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            # if parent key is not in the column_names, add parent key,value pair first
            if column_name not in column_names:
                column_names.append((column_name,v))
            # use recursive call to flatten the nested dictionaries
            column_names.extend(get_column_names(v, column_name).items())
        else:
            column_names.append((column_name, v))
    return dict(column_names)

def get_nested_value(d, key):
    """Returns dictionary with flattened key from get_column_names and appends its value.
    Example:
        d = {
            'a': {
                'b': 2,
                'c': 3,
                },
        }
        key = 'a.b'
        will return: 2
    """
    if '.' not in key:
        if key not in d:
            return None
        return d[key]
    base_key, sub_key = key.split('.', 1)
    if base_key not in d:
        return None
    sub_dict = d[base_key]
    if isinstance(sub_dict, dict):
        return get_nested_value(sub_dict, sub_key)
    elif sub_dict is None:
        return None
    else:
        print(sub_dict)
        return None

def get_row(line_contents, column_names):
    row = []
    for column_name in column_names:
        line_value = get_nested_value(
                        line_contents,
                        column_name,
                        )

        if line_value is not None:
            row.append('{0}'.format(line_value))
        else:
            row.append('')
    return row

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
            'json_file',
            type=str
            )

    args = parser.parse_args()

    json_file = args.json_file
    csv_file = '{0}.csv'.format(json_file.split('.json')[0])

    column_names = get_superset_of_column_names_from_file(json_file)
    read_and_write_file(json_file, csv_file, column_names)
