import json
from config import constants


# Load the JSON file
with open(constants.LOCALIZATION_FILE_PATH, 'r', encoding='utf-8') as file:
    localizations = json.load(file)

# Function to get the localized text and replace placeholders
def get_localized_text(key, **kwargs):
    template = localizations.get(constants.CURRENT_LANGUAGE, {}).get(key, key)
    return template.format(**kwargs)
