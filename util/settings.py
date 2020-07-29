import json


class Vars():

    def __init__(self):
        global_vars = json.loads(open('resources/global_vars.json').read())
        self.__prefix = global_vars["prefix"]
        self.__token = global_vars["token"]
        self.__sounds = global_vars["sounds"]

    def get_sounds(self):
        return self.__sounds

    def get_prefix(self):
        return self.__prefix

    def get_token(self):
        result = self.__token
        del self.__token
        return result