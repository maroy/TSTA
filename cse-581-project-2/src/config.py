import yaml


class Config:

    def __init__(self):
        with open("config.yaml", "rb") as cfg_file:
            self.data = yaml.load(cfg_file)

    def commit_seconds(self):
        return int(self.data["commit_seconds"])

    def db_size_limit(self):
        return int(self.data["db_size_limit"])

    def data_folder(self):
        return str(self.data["data_folder"])

    def key_words(self):
        return [str(x) for x in list(self.data["key_words"])]

    def languages(self):
        return [str(x) for x in list(self.data["languages"])]