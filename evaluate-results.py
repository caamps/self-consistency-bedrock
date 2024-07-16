import json
import re

def lambda_handler(event, context):
    array = event['node']['inputs'][0]['value']
    
    answers = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0}
    for item in array:
        match = re.search(r'gabarito: letra (\w)', item.lower())
        if match:
            letter = match.group(1)
            answers[letter] += 1
    
    string = ''
    for letter in answers.keys():
        string += f"{letter}: {answers[letter]} escolhas.\n"
    
    return string
