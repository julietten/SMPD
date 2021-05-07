import json
import boto3
from datetime import datetime
from decimal import Decimal

db = boto3.resource('dynamodb')
table = db.Table('smpd_399_timestamp')

client = boto3.client(
    'iot-data',
    region_name='us-east-1',
    verify=False
)

def lambda_handler(event, context):

    if event['decoded']['status'] != 'success':
        return {
            'success': False,
            'reason': 'failed to decode'
        }

    soil_moisture = event['decoded']['payload'][0]['value']
    humidity = event['decoded']['payload'][1]['value']
    temperature = event['decoded']['payload'][2]['value']
    rainwater = event['decoded']['payload'][3]['value']
    device_eui = event['dev_eui']
    timestamp = round(event['reported_at']/1000)
    date_string = datetime.fromtimestamp(timestamp).isoformat()

    row = {
        'timestamp': date_string,
        'dev_eui': device_eui,
        'humidity': int(humidity),
        'reported_at': str(timestamp),
        'soil_moisture': soil_moisture,
        'temperature': int(temperature),
        'rainwater': rainwater
    }
    
    result = {'success':True}
    
    response = table.put_item(Item=row)
    result['result'] = response
    
    table.put_item(Item=row)
    
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        result['success'] = False

    return result
