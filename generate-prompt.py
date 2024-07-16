import json
import boto3
import random

def lambda_handler(event, context):
    
    question = event['node']['inputs'][0]['value']
    paths = 5
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('questions-table')
    items = table.scan()['Items']
    
    prompts = ['' for i in range(paths)]
    for i in range(paths):
        random_numbers = random.sample(range(0, 7), 3)
        for r in random_numbers:
            prompts[i] += items[r]['question'] + '\n'
    
    for i in range(paths):
        prompts[i] += 'Pergunta: ' + question + '\nResposta: '
    
    return prompts
