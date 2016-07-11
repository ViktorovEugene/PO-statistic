import argparse
import os


class PathAction(argparse.Action):

    def __init__(self, option_strings, dest, default=None, **kwargs):
        if not default:
            default = [os.getcwd()]
        super().__init__(option_strings, dest, default=default, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if not values:
            values = [self.default]

        files, dirs = [], []
        for path in values:
            if os.path.isdir(path):
                dirs.append(path)
            elif os.path.isfile(path):
                files.append(path)

        setattr(namespace, self.dest, dict(files=files, dirs=dirs))

parser = argparse.ArgumentParser(
    description='Collect statistic data of `*.po` translation files.'
)

parser.add_argument('path', nargs='*', action=PathAction)

if __name__ == '__main__':
    print(parser.parse_args('one two'.split()),
          parser.parse_args('tmp cli.py'.split()),
          parser.parse_args(''.split()),
          sep='\n--------------\n')
