import json
import random

def lambda_handler(event, context):
    question = event['node']['inputs'][0]['value']
    paths = 5

    with open('questions.json', 'r') as f:
        items = json.load(f)

    prompts = ['' for _ in range(paths)]
    for i in range(paths):
        random_numbers = random.sample(range(len(items)), 3)
        for r in random_numbers:
            prompts[i] += items[r]['question'] + '\n'

    for i in range(paths):
        prompts[i] += 'Pergunta: ' + question + '\nResposta: '

    print(prompts[0])

    return prompts
