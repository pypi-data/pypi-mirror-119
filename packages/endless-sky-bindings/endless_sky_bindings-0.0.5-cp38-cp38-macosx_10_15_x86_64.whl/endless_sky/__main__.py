import argparse
import sys
import os
import json

import endless_sky
from endless_sky.parser import parse_ships

parser = argparse.ArgumentParser(
    prog='python -m mymodule',
    description="Endless Sky utilities powered by the actual Endless Sky codebase."
)
parser.add_argument('--version', action='store_true')
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='additional help',
                                   dest="subcommand")

parse_parser = subparsers.add_parser('parse', description='Parse a set of data files')
parse_parser.add_argument("file")
parse_parser.add_argument("--resources", required=True)
parse_parser.add_argument("--config", required=False, default=None)
parse_parser.add_argument("--format", default='pretty', help='pretty (default), json, or dict')

run_parser = subparsers.add_parser('run', description='Run endless sky (this pip-installed one) passing arguments through')
run_parser.add_argument('rest', nargs=argparse.REMAINDER)

subparsers.add_parser('version')

args = parser.parse_args()
print(args)
if args.version or args.subcommand == "version":
    print(endless_sky.version)
    sys.exit(0)
elif not args.version and not args.subcommand:
    parser.print_help()
    sys.exit(0)

# when analyzing a save game file, you can only use installed plugins
# if the saved game is in the save game folder!

# we need to be able to discover existing endless sky installations
# or have an endless sky repo manually specified.
# Later, have a script that does a zip download somewhere https://github.com/endless-sky/endless-sky/archive/1873fd9ee9a9ad6a4fd210fe03f8d5a6fc7abc25.zip
# Where do these get downloaded to? I dunno, where does nltk put its datasets?
# Maybe a .endless-sky-python-assets in home? Maybe use config dir logic?

if args.subcommand == 'parse':
    print("let's parse a file or resources directory:", args.file)
    if not os.path.exists(args.file):
        print("that file does not exist!")
        exit(1)
    output = parse_ships(
            args.file,
            format=args.format,
            resources=args.resources,
            config=args.config)
    print(output)
elif args.subcommand == 'run':
    from endless_sky import bindings
    bindings.main(['progname'] + args.rest)
