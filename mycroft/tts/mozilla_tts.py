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
import requests
from .tts import TTS, TTSValidator
from mycroft.util.log import LOG

class MozillaTTS(TTS):
    """Interface to MozillaTTS."""
    def __init__(self, lang, config):
        super(MozillaTTS, self).__init__(lang, config, MozillaTTSValidator(
            self), 'wav')

    def get_tts(self, sentence, wav_file):
        """Fetch tts audio using http(s)."""
        r = requests.get(self.config.get("api_url"), params={'text': sentence})
        with open(wav_file, 'wb') as f:
            f.write(r.content)
        return (wav_file, None)  # No phonemes


class MozillaTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(MozillaTTSValidator, self).__init__(tts)

    def validate_lang(self):
        # mozilla TTS can support any language, it only depends on the model used
        pass

    def validate_connection(self):
        try:
            requests.get(self.tts.config.get("api_url"), params={'text': "test"})
        except Exception:
            raise Exception(
                'Could not reach MozillaTTS server. Please check your '
                'internet connection or the server.')

    def get_tts_class(self):
        return MozillaTTS
