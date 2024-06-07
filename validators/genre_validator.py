import json
from jsonschema import validate


class GenreValidator:
    def get_add_genre_schema(self):
        with open("schemes/add_genre.schema.json", "r") as file:
            schema = json.load(file)

        return schema

    def validate_add_genre(self, json_data):
        schema = self.get_add_genre_schema()
        validate(instance=json_data, schema=schema)

    def get_edit_genre_schema(self):
        with open("schemes/edit_genre.schema.json", "r") as file:
            schema = json.load(file)

        return schema

    def validate_edit_genre(self, json_data):
        schema = self.get_edit_genre_schema()
        validate(instance=json_data, schema=schema)