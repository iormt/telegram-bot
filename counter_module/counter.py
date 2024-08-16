import json
import os
from constants_module import constants


counter_data = {}



def save_counter_data():
    with open(constants.COUNTER_DATA_PATH, 'w') as file:
        json.dump(counter_data, file)


if os.path.exists(constants.COUNTER_DATA_PATH):
    with open(constants.COUNTER_DATA_PATH, 'r') as file:
        counter_data = json.load(file)