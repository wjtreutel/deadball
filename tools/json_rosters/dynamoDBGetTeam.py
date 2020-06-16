import boto3
from pprint import pprint
import json
  
def get_team(title, year, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")

    table = dynamodb.Table('Teams')

    try:
        response = table.get_item(Key={'abbreviation': "GTY", 'year': 2019})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']
        
        
client = boto3.client('dynamodb')
table = client.list_tables()

movie = get_team("The Big New Movie", 2015,)
if movie:
    print("Get movie succeeded:")
    for player in movie['players']:
        print(player['full_name'])
    pprint(movie)