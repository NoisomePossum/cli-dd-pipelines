'''
Command-line tool for copying pipelines
from one Datadog org to another
'''

import os
import argparse
import requests
import keys

parser = argparse.ArgumentParser(description='Sends logs to Datadog'
                                 ' from your command line.'
                                 ' Accepts a simple string or a text file.')

parser.add_argument('--sourcekey', dest='sourcekey',
                    help='set the api key of the org to copy pipelines from')
parser.add_argument('--destkey', dest='destkey',
                    help='set the api key of the org to copy pipelines to')
args = parser.parse_args()


def main():
    create_pipelines()


def create_pipelines():

    print('Copying pipelines from org with api key '+args.sourcekey+' to org with api key '+args.destkey)

if __name__ == "__main__":
    main()
