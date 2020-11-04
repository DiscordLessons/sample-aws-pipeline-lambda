import json
import subprocess
import sys
import time

# Returns the 'hours' value supplied by the API.
def hello_world(event, context):
    input_time = event['queryStringParameters']['hours']
    return {
    'statusCode': 200,
    'body': "Hello Riiid Labs! Hours: " + input_time
    }
