#!/usr/bin/env python
import sys

from imars_etl.cli import main


def _main():
    main(sys.argv[1:])


if __name__ == "__main__":
    _main()
