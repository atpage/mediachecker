#!/usr/bin/env python3

import argparse
import os
import re
import fnmatch

from mediachecker import AVFile

default_extensions = ['.avi', '.mkv', '.mp4', '.mpg', '.m4v']
# TODO: ['.divx', '.m2ts', '.ts', '.vob', '.webm', '.wmv']


def main():
    parser = argparse.ArgumentParser(
        description='Check media file(s) for errors.',
    )
    parser.add_argument(
        '-r',
        '--recursive',
        action='store_true',
        default=False,
        help='search for media files recursively (default: False)',
    )
    parser.add_argument(
        '-l',
        '--write-log',
        action='store_true',
        default=False,
        help='save results to log file(s) alongside media (default: False)',
    )
    parser.add_argument(
        '-f',
        '--full',
        action='store_true',
        default=False,
        help='check all tracks, not just first audio track (default: False)',
    )
    parser.add_argument('path-or-file', help='file or directory to check')
    # TODO: options to:
    #  - specify extensions to check
    #  - log whole process / results to a single file?
    #  - skip files with existing logs (but use the existing log as good/bad flag)
    #  - accept a list of files / paths instead of a single one
    args = parser.parse_args()
    path_or_file = getattr(args, 'path-or-file')
    method = 'full' if args.full else 'first_audio_track'
    if os.path.isdir(path_or_file):
        files_are_good = check_path(
            base_dir=path_or_file,
            extensions=default_extensions,
            write_logs=args.write_log,
            method=method,
            recursive=args.recursive,
        )
        if files_are_good:
            print("Files all look good!")
        else:
            print("At least one file looks corrupt!")
    elif os.path.isfile(path_or_file):
        file_is_good = check_file(
            filename=path_or_file,
            write_log=args.write_log,
            method=method,
        )
        if file_is_good:
            print("File looks good!")
        else:
            print("File looks corrupt!")
        # TODO: catch warning?
    else:
        raise FileNotFoundError()
    # TODO: print result(s) / exit (code?)


def check_file(filename, write_log, method):
    """returns True if file is good."""
    f = AVFile(filename)
    file_is_good = f.is_good(method=method, write_log=write_log)
    return file_is_good


def check_path(base_dir, extensions, write_logs, method, recursive):
    """returns True if all files found are good."""
    results = []
    for extension in extensions:
        if recursive:
            matching_files = find_files_recursive(base_dir, '*' + extension)
        else:
            matching_files = find_files_nonrecursive(base_dir, '*' + extension)
        for filename in matching_files:
            # print(filename)  # debugging
            status = check_file(
                filename=filename,
                write_log=write_logs,
                method=method,
            )
            results.append(status)
    # print("tested check_path().")  # debugging
    return all(results)


def find_files_nonrecursive(base_dir, globexpression):
    """case-insensitive search based on https://stackoverflow.com/a/12213141/1063154"""
    reg_expr = re.compile(fnmatch.translate(globexpression), re.IGNORECASE)
    list_path = [
        i for i in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, i))
    ]
    result = [os.path.join(base_dir, j) for j in list_path if re.match(reg_expr, j)]
    return result


def find_files_recursive(base_dir, globexpression):
    """recursive, case-insensitive search based on https://stackoverflow.com/a/12213141/1063154"""
    result = []
    reg_expr = re.compile(fnmatch.translate(globexpression), re.IGNORECASE)
    for root, dirs, files in os.walk(base_dir, topdown=True):
        result += [os.path.join(root, j) for j in files if re.match(reg_expr, j)]
    return result


if __name__ == '__main__':
    main()
