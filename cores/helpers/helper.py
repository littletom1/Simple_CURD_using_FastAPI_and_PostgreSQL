from datetime import datetime
import re, os
from pathlib import Path
from decouple import config
from functools import wraps
from fastapi import HTTPException
import uuid

def get_uuid_id():
    return str(uuid.uuid4())

def with_err_log(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # my_header = request.headers.get('my-header')
        # print(request.headers)
        # my_header will be now available in decorator
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=e.status_code,
                        detail=e.detail)

    return wrapper
async def get_admin():
    from cores.services.user_client import UserClient
    admin = await UserClient().search('email', config('ADMIN_MAIL'))
    return admin

def sqlachemy_obj_to_dict(obj):
    dictret = obj.__dict__
    if '_sa_instance_state' in dictret:
        dictret.pop('_sa_instance_state', None)
    if 'created_at' in dictret:
        dictret.pop('created_at', None)
    if 'updated_at' in dictret:
        dictret.pop('updated_at', None)
    if 'deleted_at' in dictret:
        dictret.pop('deleted_at', None)
    return dictret

def clean_str_to_import(data):
    if type(data) is not str:
        data = str(data)
    data = data.strip()
    data = data.replace('\n', '. ')
    data = data.replace('"', "'")
    return data

def get_current_time_as_int() -> int:
    now = datetime.now()
    current_time = now.timestamp()
    return int(current_time)

def convert_datetime_to_timestamp(y, m, d, h=0, i=0 ,s=0) -> int:
    now = datetime(y, m, d, h, i , s)
    current_time = now.timestamp()
    return int(current_time)

def check_is_roman(subject):
    pattern = "M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})"
    if subject:
        if re.fullmatch(pattern, subject):
            return True
        return False

def number_to_roman(number):
    list_map = {
        'XL': 40,
        'X': 10,
        'IX': 9,
        'V': 5,
        'IV': 4,
        'I': 1,
    }
    number = int(number)
    return_value = ''
    while number > 0:
        for roman, num_int in list_map.items():
            if number >= num_int:
                number = number - num_int
                return_value = return_value + roman
                break
    return return_value

def open_file_as_root_path(file_path):
    # root_path = os.path.dirname(__file__)
    path_root = Path(__file__).parents[2]
    abs_file_path = os.path.join(path_root, file_path)
    return open(abs_file_path, 'rb')

def write_to_json(file_path, content):
    path_root = Path(__file__).parents[2]
    abs_file_path = os.path.join(path_root, file_path)
    f = open(abs_file_path + '/output.json', "w")
    f.write(content)
    print(abs_file_path)

def object_to_dict(obj, with_relation = False, exclude_relation=[], found=None):
    from sqlalchemy.orm import class_mapper
    if found is None:
        found = set()
    mapper = class_mapper(obj.__class__)
    columns = [column.key for column in mapper.columns]
    get_key_value = lambda c: (c, getattr(obj, c).isoformat()) if isinstance(getattr(obj, c), datetime) else (c, getattr(obj, c))
    out = dict(map(get_key_value, columns))
    if with_relation:
        for name, relation in mapper.relationships.items():
            if relation not in found and str(relation) not in exclude_relation:
                found.add(relation)
                related_obj = getattr(obj, name)
                if related_obj is not None:
                    if relation.uselist:
                        out[name] = [object_to_dict(child, with_relation, exclude_relation, found) for child in related_obj]
                    else:
                        out[name] = object_to_dict(related_obj, with_relation, exclude_relation, found)
    return out