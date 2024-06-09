import json

from jsonschema import validate


class UserValidator:
    def get_add_user_schema(self):
        with open("schemes/add_user.schema.json", "r") as file:
            schema = json.load(file)

        return schema

    def validate_add_user(self, json_data):
        schema = self.get_add_user_schema()
        validate(instance=json_data, schema=schema)

    def get_edit_user_schema(self):
        with open("schemes/edit_user.schema.json", "r") as file:
            schema = json.load(file)

        return schema

    def validate_edit_user(self, json_data):
        schema = self.get_edit_user_schema()
        validate(instance=json_data, schema=schema)
