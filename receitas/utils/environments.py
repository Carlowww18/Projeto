import os

def get_env_variable(variable_name, default_value=''):
    return os.environ.get(variable_name, default_value)

def parse_comma_str_to_list(comma_str):
    if not comma_str or not isinstance(comma_str, str):
        return []
    return [string.strip() for string in comma_str.split(',') if string]

print(parse_comma_str_to_list(get_env_variable('ALLOWED_HOSTS')))