
import os
import subprocess
import shlex
from warnings import warn

# import datetime as dt
# import glob
# import re
# import fnmatch
# import pathlib

class AVFile:

    def __init__(self, filename=None):
        self.filename = filename  # TODO: ensure string or None

    def is_good(self, method='first_audio_track'):

        if self.filename is None:
            raise ValueError('No filename was given.')

        if not os.path.isfile(self.filename):
            raise FileNotFoundError

        # TODO: ensure that ffmpeg is installed

        if method == 'first_audio_track':
            command = "ffmpeg -v error -i %s -map 0:1 -f null -" % (shlex.quote(self.filename))
        else:
            raise ValueError("'first_audio_track' is the only method currently supported.")
            # TODO: See
            #   https://superuser.com/questions/100288/how-can-i-check-the-integrity-of-a-video-file-avi-mpeg-mp4
            # for some more method ideas.

        try:
            output = subprocess.check_output(
                command,
                shell = True,
                stderr = subprocess.STDOUT,
            )
        except subprocess.CalledProcessError:
            warn("Couldn't process %s" % self.filename)
            return None

        return len(output) == 0
