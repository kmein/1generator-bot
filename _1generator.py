from functools import reduce
from random import random
import csv

class Replacement:

    def __init__(self, search: str, replace: str, probability: float):
        self.search = search
        self.replace = replace
        self.probability = probability

    def from_row(row):
        return Replacement(row[0], row[1], float(row[2]))

    def __repr__(self) -> str:
        return "Replacement({}, {}, {})".format(repr(self.search), repr(self.replace), self.probability)

    def apply(self, text: str) -> str:
        parts = text.split(self.search)
        output = ""
        for i, part in enumerate(parts):
            if i != len(parts) - 1:
                if conditioned(self.probability):
                    output += part + self.replace
                else:
                    output += part + self.search
            else:
                output += part
        return output

def conditioned(probability: float) -> bool:
    return (1 - probability) <= random()

def get_replacements(path: str) -> list:
    vongreader = csv.reader(open(path, newline=""))
    return [Replacement.from_row(row) for row in vongreader]

def translate_with(replacements: list, text: str) -> str:
    return reduce(lambda t, r: r.apply(t), replacements, text)

if __name__ == "__main__":
    import sys
    repls = get_replacements("vong.csv")
    inp = sys.stdin.read()
    sys.stdout.write(translate_with(repls, inp))
