import json


class Vars():

    def __init__(self):
        global_vars = json.loads(open('resources/global_vars.json').read())
        self.__prefix = global_vars["prefix"]
        self.__token = global_vars["token"]

    def get_prefix(self):
        return self.__prefix

    def get_token(self):
        return self.__token