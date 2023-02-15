import argparse
from typing import List

class ArgsHint(argparse.Namespace):
    test: List[str]

parser = argparse.ArgumentParser()

parser.add_argument("--test", type=str, nargs="+", default="ABC")
args: ArgsHint = parser.parse_args()


print(type(args.test))
for i in args.test:
    print(i)