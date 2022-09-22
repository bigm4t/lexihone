from os import listdir, environ
from os.path import isfile, join
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ""
from pygame import mixer, time
from io import BytesIO
from argparse import ArgumentParser
from random import choices
from pydub import AudioSegment
from gtts import gTTS


def topic_picker(topics):
    topic = choices(topics, weights = [tp.score for tp in topics], k = 1)
    return topic[0]

def read_word(word):
    tts = gTTS(text=word, lang='de')#check gtts doc for other possible languages
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    #For some reason pygame only reads wav and gTTS only exports mp3
    sound = AudioSegment.from_mp3(fp)
    sound.export(fp, format="wav")

    mixer.init()
    mixer.music.load(fp)
    mixer.music.play()
    while mixer.music.get_busy():
        time.Clock().tick(10)

def get_filename():
    parser = ArgumentParser()
    parser.add_argument('-fIn', help="Lexibank (.csv)", type=str, nargs="+")
    path = "./data/"

    filename = parser.parse_args().fIn

    if filename is None:
        filename = [path+f for f in listdir(path) if isfile(join(path, f)) and f[-4:]==".csv"]

    return filename
