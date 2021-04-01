#!/usr/bin/python3

DEBUG_FLAG = False

import json
import os
import sys
import logging
from datetime import datetime
import EasyBlinkt

LOGGING_FMT: str = '%(levelname)s [%(asctime)s] %(message)s'
DEFAULT_LOG: str = f'{sys.argv[0]}.log'

if DEBUG_FLAG:
    CURRENT_TIME = "0600"
    TIMEOUT_LENGTH = 180
else:
    CURRENT_TIME = datetime.now().strftime('%H%M')
    TIMEOUT_LENGTH = 43200


def main(json_file_location: str):
    exit_code = 1
    with open(json_file_location) as f:
        json_data = json.load(f)

    json_data = json_data.get(CURRENT_TIME, None)

    if json_data is not None:
        try:
            EasyBlinkt.setBlinktLight(
                light_number = int(json_data['Light'])
                ,brightness_level = float(json_data['Intensity'])
                ,color = [int(color) for color in json_data['Color']]
                ,duration = int(json_data['Duration']) * 60
            )

            exit_code = 0
        except:
            logging.exception('Error while trying to set blinkt light.')
            exit_code = 10
    else:
        logging.info(f'No json data found for {CURRENT_TIME}.')

    return(exit_code)


if __name__ == '__main__':
    exit_code = 1

    if (len(sys.argv) >= 1):

        logging_dict = {
            'level': logging.DEBUG if DEBUG_FLAG else logging.INFO
            ,'format': LOGGING_FMT
            ,'filename': DEFAULT_LOG
        }

        if (len(sys.argv) > 2):
            if os.path.isdir(os.path.dirname(sys.argv[2])):
                print(f'Outputting log data to {sys.argv[2]}')
                logging_dict.update({
                    'filename': sys.argv[2]
                })
            else:
                print(f'Unable to write to logfile location {sys.argv[2]}! Using default logfile {DEFAULT_LOG}.')

        logging.basicConfig(**logging_dict)

        if (os.path.isfile(sys.argv[1])):
            exit_code = main(json_file_location = sys.argv[1])
        else:
            logging.critical(f"Unfortunately, \"{sys.argv[1]}\" isn't a valid json file.  I'm sorry!")
    else:
        logging.warning('Usage: <script> [json config file]')

    exit(exit_code)
