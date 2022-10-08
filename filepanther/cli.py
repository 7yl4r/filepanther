"""
Define CLI interface using argparse.

"""
from argparse import ArgumentParser
import argparse
import logging
import sys
import textwrap

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
    # logger.critical('c')
    # logger.warning('w')
    # logger.info('i')
    # logger.debug('d')
    # logger.trace('t')
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
        help='addtnl help for subcommands: `filepanther $subcommand -h`'
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
        formatter_class=argparse.RawTextHelpFormatter,
        help=textwrap.dedent('''\
            Extract metadata from a filepath. \n
            Usage Examples: \n
                python3 filepanther -q parse \ \n
                    /srv/imars-objects/rookery/Processed/wv_classMaps_rgb/\
            20180501T160614_01_P003_WV02_ClassificMap_fullClass_Rookery\
            .tif \ \n 
                    --pattern /srv/imars-objects/rookery/Processed/\
            wv_classMaps_rgb/%%Y%%m%%dT%%H%%M%%S_{number}_P{pass_n}_\
            WV{sat_n}_ClassificMap_fullClass_Rookery.tif \ \n
            > metadata.json
        ''')
    )
    parser_parse.set_defaults(func=filepanther.parse_filepath)
    parser_parse.add_argument("filepath")
    parser_parse.add_argument("--type_of_file", "-t")
    parser_parse.add_argument("--pattern", "-p")


    parser_format = subparsers.add_parser(
        "format",
        help="fill filepath patterns using metadata"
    )
    parser_format.set_defaults(func=filepanther.format_filepath)
    parser_format.add_argument("--pattern")
    parser_format.add_argument("--json_file")

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
