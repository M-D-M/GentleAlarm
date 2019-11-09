#!/usr/bin/python3

DEBUG_FLAG = False

import json, os, sys, subprocess
from datetime import datetime

if DEBUG_FLAG:
    CURRENT_TIME = "0600"
    TIMEOUT_LENGTH = 180
else:
    CURRENT_TIME = datetime.now().strftime('%H:%M')
    TIMEOUT_LENGTH = 43200

json_config_file = ''
exit_code = 1

def main():
    exit_code = 1
    with open(json_config_file) as f:
        json_data = json.load(f)

    json_data = json_data.get(CURRENT_TIME, None)

    if json_data is not None:
        color_data = ','.join(json_data['Color'])
        try:
            subprocess.run([
                'setBlinkt.py'
                ,json_data['Light']
                ,json_data['Intensity']
                ,f'{color_data}'
                ,json_data['Duration']
            ]
            ,timeout=TIMEOUT_LENGTH)

            exit_code = 0
        except subprocess.TimeoutExpired:
            print('Timeout exceeded while waiting for setBlinkt.py to run.')
            exit_code = 10
        except subprocess.SubprocessError:
            print('Error code received when trying to run setBlinkt.py.')
            exit_code = 20
    else:
        print(f'No json data found for {CURRENT_TIME}.')

    return(exit_code)
        

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        if (os.path.isfile(sys.argv[1])):
            json_config_file = sys.argv[1]
            exit_code = main()
        else:
            print(f"Unfortunately, \"{sys.argv[1]}\" isn't a valid json file.  I'm sorry!")
    else:
        print('Usage: <script> [json config file]')

    exit(exit_code)
