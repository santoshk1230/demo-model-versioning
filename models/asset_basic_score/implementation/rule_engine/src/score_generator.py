import warnings

warnings.filterwarnings("ignore")
from abc import ABC
from util.rule import get_score
import json


class ScoreGenerator:
    def __init__(self, data: dict = None, payload: dict = None):
        self.data = data
        input_data = payload.input
        if input_data:
            self.input_data = input_data
            self.data["input_data"] = dict(input_data)
        self.client_klass = self.get_client_klass(payload)
        self.rule_config = self.get_client_rule_config(payload)

    def get_client_klass(self, payload: dict):
        client_klass_name = (
            f"{payload.client_name}_{str(payload.m_version).replace('.', '_')}"
        )
        module = __import__(
            f"model.{client_klass_name}",
            fromlist=[client_klass_name],
        )
        client_klass = getattr(module, client_klass_name) #.upper())
        return client_klass

    def get_client_rule_config(self, payload: dict):
        client_klass_name = (
            f"{payload.client_name}_{str(payload.m_version).replace('.', '_')}"
        )
        file_path = f"config/{client_klass_name}.json"
        with open(file_path, "r") as file:
            rule_data = json.load(file)
        rule_config = rule_data.get("rules", [])
        return rule_config

    def get_custom_ip_data(self, rule_configs):
        ip_data = dict()
        field_error = ""
        print(self.data)
        for rule_config in rule_configs:
            col_mapping = rule_config["values"]
            for col_name, mapping in col_mapping.items():
                keys = mapping.split(".")
                value = self.data
                for key in keys:
                    if key not in value:
                        field_error = f"{key} not present"
                        return ip_data, field_error
                    value = value[key]
                ip_data[col_name] = value
        return ip_data, field_error

    def get_data_as_per_rules(self):
        rules = self.client_klass().rules
        ip_data, field_error = self.get_custom_ip_data(self.rule_config)
        if field_error != "":
            return {"field_error": field_error}
        response = get_score(ip_data, rules)
        return response