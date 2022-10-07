"""
Define CLI interface using argparse.

"""
from argparse import ArgumentParser
import logging
import sys

import filepanther
from .util.config_logger import config_logger

def main(argvs):
    args = parse_args(argvs)
    config_logger(args.verbose, args.quiet)
    logger = logging.getLogger("{}.{}".format(
        __name__,
        sys._getframe().f_code.co_name)
    )
    HELLO = '=== IMaRS file-path-handling Tool "filepanther" v{} ==='.format(
        filepanther.__version__
    )
    logger.info(HELLO)
    logger.info('=' * len(HELLO))
    # # log test:
    logger.critical('c')
    logger.warning('w')
    logger.info('i')
    logger.debug('d')
    logger.trace('t')
    # exit()
    if args.version:
        print("v{}".format(filepanther.__version__))
        exit()
    else:
        del args.version
        try:
            fn = args.func
        except AttributeError:
            parse_args([""])
        del args.func
        result = fn(**vars(args))

    return result


def parse_args(argvs):
    # print(argvs)
    # =========================================================================
    # === set up arguments
    # =========================================================================
    parser = ArgumentParser(description='Interface for IMaRS ETL operations')

    # === arguments for the main command
    parser.add_argument(
        "-v", "--verbose",
        help="increase output verbosity",
        action="count",
        default=0
    )
    parser.add_argument(
        "-q", "--quiet",
        help="output only results",
        action="store_true"
    )
    parser.add_argument(
        "-V", "--version",
        help="print version & exit",
        action="store_true"
    )

    # =========================================================================
    # === subcommands
    # =========================================================================
    subparsers = parser.add_subparsers(
        title='subcommands',
        description='usage: `filepanther $subcommand` ',
        help='addtnl help for subcommands: `imars-etl $subcommand -h`'
    )

    # # === extract
    # parser_extract = subparsers.add_parser(
    #     'extract',
    #     help='download file from data warehouse'
    # )
    # parser_extract.set_defaults(func=extract, **EXTRACT_DEFAULTS)
    # parser_extract.add_argument("sql", **SQL)


    parser_parse = subparsers.add_parser(
        "parse",
        help="extract metadata from filepath"
    )
    parser_parse.set_defaults(func=filepanther.parse)
    parser_parse.add_argument("filepath")
    parser_parse.add_argument("--type_of_file", "-t")

    # ===
    args = parser.parse_args(argvs)
    try:
        args.func
    except AttributeError:
        try:
            args.version
        except AttributeError:
            SEP = "\n-------------------------------------------------------\n"
            print(SEP)
            parser.print_help()
            print(SEP)
            raise ValueError(
                "\n\n\tSubcommand is required. See help above."
            )
    # =========================================================================
    return args
