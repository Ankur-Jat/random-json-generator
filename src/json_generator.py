#!/usr/bin/python
import copy
import datetime
import json
import os
from pprint import pprint
import random
import string

class JsonGenerator():
    # JsonGenerator class takes schema_file argument in it's constructer.
    # It exposes one public method that is use to build JSON data
    def __init__(self, schema_file, file_folder_location, file_count=1,
        objects_per_file=10, custome_methods=[]):
        with open(schema_file) as f:
            data = json.load(f)
            self.__schema = data["_schema"]
            self.__schema["file_count"] = file_count
            self.__schema["objects_per_file"] = objects_per_file
            self.__ref = data["_ref"]
            del data
        self.file_folder_location = file_folder_location
        self.__custom_methods = custome_methods
        self.__validate_schema()

    def __validate_schema(self):
        # Add validation code of schema here
        pass

    def __run_custom_methods(self, main_object):
        # A middleware that run after generating main object
        for custom_method in self.__custom_methods:
            custom_method(main_object)

    def __generate_main_object(self):
        if self.__schema["datatype"] == "object":
            main_object = self.__generate_object(self.__ref["object_main"]["data"])
        else:
            main_object = getattr(self, "_%s__generate_%s"%(self.__class__.__name__, 
                self.__ref["object_main"]["datatype"]))(self.__ref["object_main"])
        self.__run_custom_methods(main_object)
        return copy.deepcopy(main_object)

    def __generate_object(self, data):
        inner_data = {}
        for key in data.keys():
            if data[key]["datatype"] == "object":
                inner_data[key] = self.__generate_object(self.__ref[data[key]["reference"]]["data"])
            else:
                inner_data[key] = getattr(self, "_%s__generate_%s"%(self.__class__.__name__,
                    data[key]["datatype"]))(data[key])
        return copy.deepcopy(inner_data)

    def __generate_array(self, data):
        array = []
        for _ in range(random.randint(data["min"], data["max"])):
            if data["item_datatype"] == "object":
                generated_data = getattr(self, "_%s__generate_%s"%(self.__class__.__name__, 
                    data["item_datatype"])
                )(self.__ref[data["item_data_helper"]["reference"]]["data"])
            else:
                generated_data = getattr(self, "_%s__generate_%s"%(self.__class__.__name__, 
                    data["item_datatype"]))(self.__ref[data["item_data_helper"]])
            array.append(generated_data)
        return copy.deepcopy(array)
    
    def __generate_datetime(self, data):
        datetime_value = datetime.datetime.now()
        if data.get("format"):
            datetime_value = datetime_value.strftime(data["format"])
        else:
            datetime_value = str(datetime_value)
        return datetime_value

    def __generate_string(self, data):
        if data.get("choice"):
            random_string = random.choice(data["choice"])
        elif data.get("prefix"):
            prefix_value = data["prefix"]["ref"]
            if data["prefix"].get("range"):
                prefix_value += str(random.randint(data["prefix"]["range"]["min"], data["prefix"]["range"]["max"]))
            elif data["prefix"].get("choice"):
                prefix_value += str(random.choice(data["prefix"]["choice"]))
            random_string = prefix_value
        else:
            random_string = ''.join(
                [random.choice(string.ascii_lowercase) for _ in range(random.randint(data["min"], data["max"]))]
            )
        if data.get("to_upper"):
            random_string = random_string.upper()
        return random_string

    def __generate_int(self, data):
        if data.get("choice"):
            return random.choice(data["choice"])
        elif "fix" in data.keys():
            return data["fix"]
        else:
            return random.randint(data["min"], data["max"])
    
    def generate_random_data(self):
        total_objects_count = self.__schema["file_count"] * self.__schema["objects_per_file"]
        print("Starting generating data for", total_objects_count, "objects")
        file_count = 1
        while file_count <= self.__schema["file_count"]:
            generated_json_data = []
            with open(self.file_folder_location + "file_" + str(file_count) + ".json", "w") as json_file:
                objects_per_file = self.__schema["objects_per_file"]
                while objects_per_file > 0:
                    generated_json_data.append(
                        self.__generate_main_object()
                    )
                    objects_per_file -= 1
                json.dump(generated_json_data, json_file)
            print("\nfile", file_count, "is generated\n")
            file_count += 1
        print("Generated", total_objects_count, "objects. Just for you!")


if __name__ == '__main__':
    random_object = JsonGenerator()
    random_object.generate_random_data()