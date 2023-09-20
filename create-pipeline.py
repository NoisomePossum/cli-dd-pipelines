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
    if check_creds():
        create_pipelines()
    
def check_creds():
    if None in (args.source_api_key, args.source_app_key, args.dest_api_key, args.dest_app_key, args.pipeline_id):
        print("You are missing one of the required fields:\n- source api key\n- source app key\n- destination api key\n- destination app key\n- pipeline id")
        return False
    return True

def copy_pipeline():
    
    print("Copying pipeline from the source org")
    
    headers = {
    'DD-API-KEY': args.source_api_key,
    'DD-APPLICATION-KEY': args.source_app_key,
    'Accept': 'application/json'
    }
    url = keys.HTTP_ENDPOINT + '/' + args.pipeline_id
    
    response = requests.get(url, headers=headers)
    
    #check if the request was unsuccessful
    try:
        response.raise_for_status()
    except:
        print ('Status Code: {}'.format(response.status_code))
        if response.status_code == 429:
            limit_time = response.headers['X-RateLimit-Reset']
            print('Rate Limited - wait {} seconds before the next call'.format(limit_time))
        print ('Error Details: {}'.format(response.json()))
        return None
    return response.json()


def create_pipelines():
    
    #retrieve and format the source pipeline for the create endpoint
    source_pipeline = copy_pipeline()
    if source_pipeline:
        new_pipeline = {
            'name': source_pipeline['name'],
            'filter':{
                'query': source_pipeline['filter']['query']
            },
            'is_enabled': source_pipeline['is_enabled'],
            'processors': source_pipeline['processors']
        }
        
        print("Creating pipeline in the destination org")
        
        headers = {
        'DD-API-KEY': args.dest_api_key,
        'DD-APPLICATION-KEY': args.dest_app_key,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }
        url = keys.HTTP_ENDPOINT
        
        response = requests.post(url, data=json.dumps(new_pipeline), headers=headers)
        try:
            response.raise_for_status()
        except:
            print ('Status Code: {}'.format(response.status_code))
            if response.status_code == 429:
                limit_time = response.headers['X-RateLimit-Reset']
                print('Rate Limited - wait {} seconds before the next call'.format(limit_time))
            print (response.json())

if __name__ == "__main__":
    main()
