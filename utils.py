import os
import json
import datetime
import decimal
import numpy as np


def save_json(filename: str, data: dict) -> None:
    """
    Save data into json file in temp path.
    """
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            # 处理返回数据中有date类型的数据
            if isinstance(obj, datetime.date):
                return obj.strftime("%Y-%m-%d")
            # 处理返回数据中有datetime类型的数据
            elif isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            # 处理返回数据中有decimal类型的数据
            elif isinstance(obj, decimal.Decimal):
                return float(obj)
            elif isinstance(obj, np.int32) or isinstance(obj, np.int64):
                return int(obj)
            else:
                try:
                    return json.JSONEncoder.default(self, obj)
                except:
                    print(type(obj))
                    input()

    with open(filename, mode="w+", encoding="UTF-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False,
            cls=DateEncoder
        )

def load_json(filename: str) -> dict:
    """
    Load data from json file in temp path.
    """
    if os.path.exists(filename):
        with open(filename, mode="r", encoding="UTF-8") as f:
            data = json.load(f)
        return data
    else:
        save_json(filename, {})
        return {}

def update_json(filename: str, new_data) -> None:
    data = load_json(filename)
    if isinstance(new_data, dict):
        data.update(new_data)
    elif isinstance(new_data, list):
        data += new_data
    save_json(filename, data)

