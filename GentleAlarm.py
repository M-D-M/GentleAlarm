#!/usr/bin/python3

DEBUG_FLAG = False
LOGGING_FMT: str = '%(levelname)s [%(asctime)s] %(message)s'

import json
import os
import sys
import logging
from datetime import datetime
import EasyBlinkt


if DEBUG_FLAG:
    CURRENT_TIME = "0600"
    TIMEOUT_LENGTH = 180
else:
    CURRENT_TIME = datetime.now().strftime('%H%M')
    TIMEOUT_LENGTH = 43200

logging.basicConfig(
    level = logging.DEBUG if DEBUG_FLAG else logging.INFO
    ,format = LOGGING_FMT
)
json_config_file = ''
exit_code = 1


def main():
    exit_code = 1
    with open(json_config_file) as f:
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
    if (len(sys.argv) > 1):
        if (os.path.isfile(sys.argv[1])):
            json_config_file = sys.argv[1]
            exit_code = main()
        else:
            logging.critical(f"Unfortunately, \"{sys.argv[1]}\" isn't a valid json file.  I'm sorry!")
    else:
        logging.warning('Usage: <script> [json config file]')

    exit(exit_code)
