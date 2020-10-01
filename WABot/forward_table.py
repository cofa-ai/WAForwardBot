import json
import os


class ForwaradTable:
    def __init__(self, path):
        self.path = path
        self.table = self.read_config()

    def read_config(self):
        if not os.path.exists(self.path):
            return {}
        with open(self.path) as json_file:
            data = json.load(json_file)
            return data

    def write_config(self):
        with open(self.path, 'w') as outfile:
            json.dump(self.table, outfile)

    def add_route(self, source, dest):
        self.table[source] = dest
        self.write_config()

    def remove_route(self, source):
        rm_route = self.table.pop(source, False)
        self.write_config()
        return rm_route

    def clean_table(self):
        self.table = {}
        self.write_config()

    def like_str(self):
        return json.dumps(self.table, 
                          ensure_ascii=False,
                          indent=4)
