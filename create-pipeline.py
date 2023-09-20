'''
Command-line tool for copying pipelines
from one Datadog org to another
'''

import os
import argparse
import requests
import json
import keys

parser = argparse.ArgumentParser(description='Sends logs to Datadog'
                                 ' from your command line.'
                                 ' Accepts a simple string or a text file.')

parser.add_argument('--source_api_key', dest='source_api_key',
                    help='set the api key of the org to copy pipelines from')
parser.add_argument('--source_app_key', dest='source_app_key',
                    help='set the app key of the org to copy pipelines from')
parser.add_argument('--dest_api_key', dest='dest_api_key',
                    help='set the api key of the org to copy pipelines to')
parser.add_argument('--dest_app_key', dest='dest_app_key',
                    help='set the app key of the org to copy pipelines to')
parser.add_argument('--p_id', dest='pipeline_id', help='set the id of the pipeline to copy')
args = parser.parse_args()

def main():
    create_pipelines()

def copy_pipeline():
    
    headers = {
    'DD-API-KEY': args.source_api_key,
    'DD-APPLICATION-KEY': args.source_app_key,
    'Accept': 'application/json'
    }
    url = keys.HTTP_ENDPOINT + '/' + args.pipeline_id
    
    # get pipeline from source account
    return requests.get(url, headers=headers).json()


def create_pipelines():
    
    # todo: if the api keys or app key or pipeline id are missing stop and give an error message
       
    headers = {
    'DD-API-KEY': args.dest_api_key,
    'DD-APPLICATION-KEY': args.dest_app_key,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }
    url = keys.HTTP_ENDPOINT
    
    #format the source pipeline for the create endpoint
    source_pipeline = copy_pipeline()
    new_pipeline = {
        'name': source_pipeline['name'],
        'filter':{
            'query': source_pipeline['filter']['query']
        },
        'is_enabled': source_pipeline['is_enabled'],
        'processors': source_pipeline['processors']
    }
    
    # create pipeline in destination account 
    response = requests.post(url, data=json.dumps(new_pipeline), headers=headers)
    
    print(response.json())

if __name__ == "__main__":
    main()
