import json


class Session:
    
    def __init__(self):
        with open("session.json","r") as file:
            self.dict = json.load(file)
    
    def output(self):
        return self.dict

session = Session().output()
