import re
import sndhdr
from subprocess import Popen, PIPE, STDOUT

from application import app

class AudioSegmentor:
    def __init__(self, wave_file):
        self.wave_file = wave_file

        self._validate()
        
    def _validate(self):
        self.valid = False
        header = sndhdr.whathdr(self.wave_file);

        if header is not None:
            if header.filetype is "wav":
                self.valid = True

    def isValid(self):
        return self.valid

    def segment(self):
        command = '%s/ssad -m 1.0 -a -s -f %s %s -'
        exe_cmd = command%('/home/audioseg/audioseg-1.2.2/src/', "16000.0", self.wave_file)

        p = Popen([app.config['SSAD_PATH'],
                '-m 1.0', '-a', '-s', '-f', '16000.0', self.wave_file, '-'],
                stdin=PIPE, stdout=PIPE, stderr=STDOUT);
        output = str(p.communicate()[0])

        json = []
        output = re.split(r'\\n', output)

        for line in output:
            line = re.split(r'\s{4,}', line)
            if line[0] == "speech":
                json += {'start': line[1], 'end': line[2]},

        return json
