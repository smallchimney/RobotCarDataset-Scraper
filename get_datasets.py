'''
Gets a list of available datasets from the Oxford Robotcar Dataset website.

Matt Gadd
Mar 2019
Oxford Robotics Institute, Oxford University.

'''

import os
import sys
import requests
import re
import argparse
BASE_DIR = "/Downloads"
sys.path.append(BASE_DIR)

from scrape_mrgdatashare import datasets_url

available_sensor_types = [
    'tags',
    'stereo_centre',
    'stereo_left',
    'stereo_right',
    'vo',
    'mono_left',
    'mono_right',
    'mono_rear',
    'lms_front',
    'lms_rear',
    'ldmrs',
    'gps'
]

def absolute_sensor_type(sensor_type):
    # if sensor_type is like stereo_centre_01
    if sensor_type[-2:].isdigit():
        return sensor_type[:-3] # stereo_centre

    return sensor_type


def main(required_sensors, required_sequences):
    # open session
    session_requests = requests.session()

    # get http response from website
    result = session_requests.get(datasets_url)
    text = result.text

    # parse response text
    text_locations = [text_location.end()
                      for text_location in re.finditer(datasets_url, text)]
    datasets = [str(text[text_location:text_location + 19])
                for text_location in text_locations]

    # ignore metadata and sort unique datasets
    datasets = datasets[2:]
    datasets = sorted(list(set(datasets)))

    # write output text file
    datasets_file = "datasets.csv"
    with open(datasets_file, "w") as file_handle:
        # iterate datasets
        if required_sequences:
            filtered_datasets = (dataset for dataset in datasets if dataset in required_sequences)
        else:
            filtered_datasets = datasets
        for dataset in filtered_datasets:
            # url to dataset page
            dataset_url = datasets_url + dataset
            result = session_requests.get(dataset_url)
            text = result.text

            # parse text for sensor type
            start = [
                text_location.end() for text_location in re.finditer(
                    "download/\?filename=datasets", text)]
            sensor_types = []
            for s in start:
                ss = s
                while text[ss + 40:ss + 44] != ".tar":
                    ss += 1
                sensor_type = text[s + 41:ss + 40]
                if absolute_sensor_type(sensor_type) in required_sensors:
                    sensor_types.append(str(sensor_type))

            # write dataset entry
            file_handle.write(dataset + "," + ",".join(sensor_types) + "\n")


if __name__ == "__main__":
    # option parsing suite
    argument_parser = argparse.ArgumentParser(
        description="get_datasets input parameters")

    # specify CL args
    argument_parser.add_argument(
        "--sensors",
        dest="required_sensors",
        help="list of sensors types you want to download, separated by ' ' (default: all sensor types).\n"
            + "e.g: --sensors tags stereo_centre\n"
            + f"list of available sensor types: {available_sensor_types}",
        nargs='+',
        default=available_sensor_types
    )

    argument_parser.add_argument(
        "--sequences",
        dest="required_sequences",
        help="file with the list of sequences you want to download, one sequence by line (default: all sequences).",
        default=None
    )

    # parse CL
    parse_args = argument_parser.parse_args()
    required_sensors = set(parse_args.required_sensors)
    assert required_sensors.issubset(set(available_sensor_types)), required_sensors - set(available_sensor_types)

    required_sequences = []
    if parse_args.required_sequences:
        required_file = os.path.join(BASE_DIR, parse_args.required_sequences)
        if not os.path.exists(required_file):
            print('cannot find required file "' + required_file + '"\n')
            sys.exit()
        with open(required_file) as required:
            for line in required.readlines():
                required_sequences.append(line.strip('\n'))

    main(required_sensors, required_sequences)
