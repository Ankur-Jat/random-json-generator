#!/usr/bin/python3
# This is a helper file that helps you to generate random json data.
import multi_json_generator
import sys
import time

import argparse
import json_generator


def custom_method(main_object):
    # This formats card_index. As I want card index map with user_id
    pass
    # main_object["payment_methods"]["card_index"] = \
    #         main_object["payment_methods"]["card_index"].format(user_id=main_object["user_id"])


def generate_single_object(schema_file):
    random_object = json_generator.JsonGenerator('./example-schema.json',
        [custom_method])
    print(random_object.get_json_data())


def generate_multi_objects(schema_file, file_folder_location, file_count, objects_per_file):
    multi_json_generator.MultiJsonGenerator(schema_file, file_folder_location, file_count, objects_per_file,
     [custom_method]).generate_random_data()
    print("\n\n================================================")
    print("Data is generated. All files are saved at", file_folder_location)
    print("================================================\n\n")


def args_generator():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", help="Single object or multiple[S/m]", default="s")
    parser.add_argument("--schema", help="Schema file path", default="./example-schema.json")
    parser.add_argument("--folder", help="File folder location for multi object generation", default="./data/")
    parser.add_argument("--count", help="Number of files to generate", default=1, type=int)
    parser.add_argument("--objects", help="Number of objects per file", default=20, type=int)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = args_generator()
    if (not args.type or (args.type.lower() == 's')):
        # single object
        generate_single_object(args.schema)
    else:
        # multi objects
        start_time = time.time()
        generate_multi_objects(args.schema, args.folder, args.count, args.objects)
        print("\n\n", time.time() - start_time, "\n\n")
