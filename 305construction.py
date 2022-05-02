#!/usr/bin/python3

from sys import argv, exit
import sys

class   Construct():
    tmp = {}
    dictionary = {}
    def __init__(self, argument):
        self.fd = open(argument[1], 'r')
        self.buff = self.fd.read().rstrip().split('\n')
        for i in self.buff:
            self.dictionary[i.split(';')[0]] = {"description": i.split(';')[1],
                "duration": int(i.split(';')[2]), "list": i.split(';')[3:],
                "begin": 0, "limit": 0, "prerequisites": [[]]}

    def computeValue(self):
        def recurse(original, name):
            for i in self.dictionary[name]["list"]:
                self.dictionary[original]["prerequisites"][-1].append(i)
                recurse(original, i)
            self.dictionary[original]["prerequisites"].append([])
        for ky in self.dictionary.keys():
            recurse(ky, ky)
            self.dictionary[ky]["prerequisites"] = [i for i in self.dictionary[ky]["prerequisites"] if i]
        for i in self.dictionary:
            tmp = 0
            duration = 0
            for d in self.dictionary[i]["prerequisites"]:
                for e in d: duration += self.dictionary[e]["duration"]
                if duration > tmp: tmp = duration
                duration = 0
            self.dictionary[i]["begin"] = tmp
        for i in self.dictionary: self.tmp[i] = self.dictionary[i]["begin"]
        self.tmp = [(k, self.tmp[k]) for k in sorted(self.tmp, key=self.tmp.get)]
        self.duration = max(i[1] + self.dictionary[i[0]]["duration"] for i in self.tmp)
        tmp = {}
        for i in self.tmp:
            tmp[i[0]] = i[1]
        for key in self.dictionary:
            deadline = self.duration
            for name in self.dictionary:
                if (deadline > tmp[name] and key in self.dictionary[name]["list"]):
                    deadline = tmp[name]
            self.dictionary[key]["end"] = deadline - (
                self.dictionary[key]["begin"] + self.dictionary[key]["duration"])

    def printValue(self):
        print("Total duration of construction: {} week{}\n"
            .format(self.duration, "s" if self.duration > 1 else ""))
        [print("{} must begin {}".format(i[0],
            ("between t=" + str(i[1]) + " and t=" + str(i[1] + self.dictionary[i[0]]["end"]))
            if self.dictionary[i[0]]["end"] != 0 else "at t=" + str(i[1]))) for i in self.tmp]
        print()
        for i in self.tmp:
            print("{}\t({})\t{}{}".format(i[0], self.dictionary[i[0]]["end"],
                ' ' * i[1], '=' * self.dictionary[i[0]]["duration"]))

def main():
    if len(argv) != 2:
        print("USAGE\n\t./305construction file\n\nDESCRIPTION\n\tfile\tfile describing the tasks")
        raise ValueError("Bad Number of Args\n")
    if argv[1] == "-h":
        print("USAGE\n\t./305construction file\n\nDESCRIPTION\n\tfile\tfile describing the tasks")
        exit(0)
    obj = Construct(argv)
    obj.computeValue()
    obj.printValue()

if __name__ == "__main__":
    try:
        main()
    except ValueError:
        exit(84)
