# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# CONFIGURATION EXAMPLE
# "tts": {
#   "module": "ivonaComand",
#   "ivonaComand": {
#     "path": "~/projects/mycroft/ivona/IVONA/ivona-telecom-pc_linux-8khz-1.6.38.186-pl_maja/bin/ivonacl",
#      "params": {
#           "-l": "~/projects/mycroft/ivona/IVONA/ivona-telecom-pc_linux-8khz-1.6.38.186-pl_maja/lib/ivona/voices/64/libvoice_pl_maja.so.1.6",
#           "-x": "~/projects/mycroft/ivona/IVONA/ivona-telecom-pc_linux-8khz-1.6.38.186-pl_maja/lib/ivona/voices/vox_pl_maja8v",
#           "-c": "~/projects/mycroft/ivona/IVONA//Certificate_of_authenticity_Cityparking.ca",
#           "--encoding": "utf-8",
#           "--dur": 75,
#           "--vol": 95,
#       }
#   }
# }

import subprocess

from mycroft.tts.tts import TTS, TTSValidator
from mycroft.configuration import Configuration
from mycroft.util import LOG


class IvonaTTSComand(TTS):
    def __init__(self, lang, config):
        super(IvonaTTSComand, self).__init__(lang, config, IvonaTTSComandValidator(self))

    def get_tts(self, sentence, wav_file):
        config = Configuration.get().get("tts").get("ivonaComand")
        BIN = config.get("path", "")
        configParams = config.get("params", {})
        configParamsList = list(configParams.keys())
        arrayOfParams = [BIN, "-t", sentence]
        stringOfParams = BIN + ' -t "' + sentence + '" '
        for key in configParamsList:
            arrayOfParams.append(key)
            value = configParams[key]
            stringOfParams += str(key) + " " + str(value) + ' '
            arrayOfParams.append(str(value))

        # subprocesParams = [BIN, "-t", sentence] + arrayOfParams
        arrayOfParams.append(wav_file)
        stringOfParams += wav_file
        print(stringOfParams)

        subprocess.call(arrayOfParams)
        # subprocess.run([BIN, "-t", sentence, wav_file])
        return (wav_file, None)  # No phonemes


class IvonaTTSComandValidator(TTSValidator):
    def __init__(self, tts):
        super(IvonaTTSComandValidator, self).__init__(tts)

    def validate_lang(self):
        # TODO
        pass

    def validate_connection(self):
        try:
            config = Configuration.get().get("tts").get("ivonaComand")
            BIN = config.get("path", "")
            subprocess.call([BIN, '--help'])
        except Exception:
            raise Exception(
                'there is no Ivona')

    def get_tts_class(self):
        return IvonaTTSComand
