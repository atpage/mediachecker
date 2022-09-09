
import os
import subprocess
import shlex
from shutil import which
from warnings import warn

# import datetime as dt
# import glob
# import re
# import fnmatch
# import pathlib

class AVFile:

    def __init__(self, filename=None):
        if type(filename) != str:
            raise TypeError('filename must be a string.')
        self.filename = filename

    def is_good(self, method='first_audio_track'):
        if self.filename is None:
            raise ValueError('No filename was given.')
        if not os.path.isfile(self.filename):
            raise FileNotFoundError("Couldn't find %s" % self.filename)
        ffmpeg_path = which('ffmpeg')
        if ffmpeg_path is None:
            raise RuntimeError("Couldn't find the ffmpeg binary.")

        if method == 'first_audio_track':
            command = "ffmpeg -v error -i %s -map 0:a:0 -f null -" % (shlex.quote(self.filename))
        elif method == 'full':
            # TODO: does this actually check all streams?
            command = "ffmpeg -v error -i %s -f null -" % (shlex.quote(self.filename))
        else:
            raise ValueError("'first_audio_track' is the only method currently supported.")

        try:
            output = subprocess.check_output(
                command,
                shell = True,
                stderr = subprocess.STDOUT,
            )
            # TODO: save output
            # TODO?: stop immediately when we get output, return False
            # without checking the rest of the file?  (-xerror should
            # work for this, but will be caught below.)
        except subprocess.CalledProcessError:
            warn("Couldn't process %s" % self.filename)
            return None
        return len(output) == 0
