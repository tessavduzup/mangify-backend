import json
from jsonschema import validate


class WalletValidator:
    def get_add_wallet_schema(self):
        with open("schemes/add_wallet.schema.json", "r") as file:
            schema = json.load(file)

        return schema

    def validate_add_wallet(self, json_data):
        schema = self.get_add_wallet_schema()
        validate(instance=json_data, schema=schema)

    def get_purchase_manga_schema(self):
        with open("schemes/purchase_manga.schema.json", "r") as file:
            schema = json.load(file)

        return schema

    def validate_purchase_manga(self, json_data):
        schema = self.get_purchase_manga_schema()
        validate(instance=json_data, schema=schema)
