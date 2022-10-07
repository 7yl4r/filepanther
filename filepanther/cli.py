"""
Define CLI interface using argparse.

"""
import logging
from argparse import ArgumentParser

import filepanther


def main(argvs):
    raise NotImplementedError("CLI not yet implemented")
    args = parse_args(argvs)
    filepanther.util.config_logger(verbosity=args.verbose, quiet=args.quiet)

    logger = logging.getLogger("filepanther.{}".format(
        __name__,
    ))
    HELLO = '=== IMaRS Extract-Transform-Load Tool v{} ==='.format(
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
        fn = args.func
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
