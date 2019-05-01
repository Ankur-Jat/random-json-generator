#!/usr/bin/python3
import json
import os

from json_generator import JsonGenerator


class MultiJsonGenerator():
    def __init__(self, schema_file, file_folder_location, file_count=1,
        objects_per_file=10, custome_methods=[]):

        self.__generated_json_data = []
        self.__json_generator = JsonGenerator(schema_file, custome_methods=custome_methods)
        self.__file_folder_location = file_folder_location
        if not os.path.exists(self.__file_folder_location):
            try:
                os.mkdir(self.__file_folder_location)
            except  OSError:
                print("Unable to generate file folder location. Please, change path or given permissions")
                exit(1)
        self.__file_count = file_count
        self.__objects_per_file = objects_per_file

    def __generate_data(self):
        self.__generated_json_data.append(
            self.__json_generator.get_json_data(True)
        )

    def generate_random_data(self):
        total_objects_count = self.__file_count * self.__objects_per_file
        print("Starting generating data for", total_objects_count, "objects")
        file_count = 1
        while file_count <= self.__file_count:
            self.__generated_json_data = []
            with open(self.__file_folder_location + "file_" + str(file_count) + ".json", "w") as json_file:
                for _ in range(self.__objects_per_file):
                    self.__generate_data()
                json.dump(self.__generated_json_data, json_file)
            print("\nfile", file_count, "is generated\n")
            file_count += 1
        print("Generated", total_objects_count, "objects. Just for you!")


if __name__ == "__main__":
    MultiJsonGenerator('./example-schema.json', './data/', 2, 20).generate_random_data()