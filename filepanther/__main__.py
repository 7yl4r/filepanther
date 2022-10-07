#!/usr/bin/env python3
import sys

from filepanther.cli import main


def _main():
    return main(sys.argv[1:])


if __name__ == "__main__":
   print(_main())
