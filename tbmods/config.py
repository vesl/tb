import os

def Config():
    config = {}
    for item,value in os.environ.items():
        if item[:3] == 'TB_':
            if value.isdigit(): value = int(value)
            config[item[3:].lower()] = value
    return config