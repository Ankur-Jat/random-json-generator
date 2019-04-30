#!/usr/bin/python
# This is a helper file that helps you to generate random json data.
import json_generator

def custom_method(main_object):
    # This formats card_index. As I want card index map with user_id
    main_object["payment_methods"]["card_index"] = \
            main_object["payment_methods"]["card_index"].format(user_id=main_object["user_id"])

if __name__ == '__main__':
    random_object = json_generator.JsonGenerator('./example-schema.json',
        './data/', objects_per_file=20, custome_methods=[custom_method])
    random_object.generate_random_data()