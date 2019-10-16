"""Rename some files. For example:

* YYYYMMDD_nnn.jpg becomes IMG_YYYYMMDD_nnn.jpg
* YYYYMMDD_nnn.mp4 becomes VID_YYYYMMDD_nnn.mp4

Usage::

    python rename_img_vid.py "D:\\My\\Windows\\Path" -v

"""
import glob
import os

__all__ = []


def prepend(path, suffix, prefix, verbose=False):
    for filepath in glob.iglob(os.path.join(path, '*.' + suffix)):
        filename = os.path.basename(filepath)
        if filename.startswith(prefix):
            continue
        newname = os.path.join(path, prefix + '_' + filename)
        os.rename(filepath, newname)
        if verbose:
            print(f'{filepath} -> {newname}')


def main(path, verbose=False):
    prepend(path, 'jpg', 'IMG', verbose=verbose)
    prepend(path, 'mp4', 'VID', verbose=verbose)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Rename some files.')
    parser.add_argument('path', type=str, help='Path name')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')

    args = parser.parse_args()
    main(args.path, verbose=args.verbose)