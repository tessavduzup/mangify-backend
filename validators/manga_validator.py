import json

from jsonschema import validate


class MangaValidator:
    def get_add_manga_schema(self):
        with open("schemes/add_manga.schema.json", "r") as file:
            schema = json.load(file)

        return schema

    def validate_add_manga(self, json_data):
        schema = self.get_add_manga_schema()
        validate(instance=json_data, schema=schema)

    def get_edit_manga_schema(self):
        with open("schemes/edit_manga.schema.json", "r") as file:
            schema = json.load(file)

        return schema

    def validate_edit_manga(self, json_data):
        schema = self.get_edit_manga_schema()
        validate(instance=json_data, schema=schema)
