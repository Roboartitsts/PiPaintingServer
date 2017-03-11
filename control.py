import * from paintApparatus
import * from abb 
import json

class Control(object):
    def __init__(self, serial_connection, apparatus):
        self.serial_connection = serial_connection
        self.apparatus = apparatus

    def load_instructions(self, path_to_instructions):
        with open(path_to_instructions) as instructions:
            for instruction in json.load(instructions):
                self.instructions.append(instructions)
    