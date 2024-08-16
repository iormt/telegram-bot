import json
import os



counter_data = {}

def save_counter_data():
    with open('counter_data.json', 'w') as file:
        json.dump(counter_data, file)


if os.path.exists('counter_data.json'):
    with open('counter_data.json', 'r') as file:
        counter_data = json.load(file)