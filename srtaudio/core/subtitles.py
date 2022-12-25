
import datetime
import os

import pyttsx3
from pysubparser import parser as subparser
from pysubparser.cleaners import ascii, brackets, formatting, lower_case
from scipy.io.wavfile import read as readwav, write as writewav
import sounddevice as sd
import numpy as np



def get_subtitles(filename):
    return formatting.clean(ascii.clean(brackets.clean(
        lower_case.clean(
            subparser.parse(filename)
        )
    )))


def get_length(subtitles) -> datetime.timedelta:
    start = datetime.time()
    end = datetime.time()

    for subtitles in subtitles:
        end = max(end, subtitles.end)

    datetime.timedelta()
    fake_date = datetime.date.min

    # convert to timedelta
    duration = datetime.datetime.combine(fake_date, end) - datetime.datetime.combine(fake_date, start)
    return duration


def play_audio(data, sample_rate):
    sd.default.samplerate = sample_rate
    sd.play(data, blocking=True)



buffer_file = "buffer.wav"

def read(filename, voice, outputfile):
    engine = pyttsx3.init()

    if voice is not None:
        engine.setProperty('voice', voice)

    length = get_length(get_subtitles(filename))

    print(f'Creating an audio file lasting {length.seconds} s')

    sample_rate = None
    audio = None

    def generate_audio_buffer(sample_rate):
        sample_count = length.seconds * sample_rate
        
        print(f'Sample rate is {sample_rate}')
        print(f'Audio has {sample_count} samples')
        print('Generating:')
        print()
        
        return np.empty((sample_count,), dtype=np.int16)

    for subtitle in get_subtitles(filename):

        t = subtitle.text
        i = subtitle.index
        s = subtitle.start
        e = subtitle.end

        engine.save_to_file(t , buffer_file)
        engine.runAndWait()

        sr, data = readwav(buffer_file)

        if sample_rate is not None:
            assert sample_rate == sr, "Sample rate should not change during generation!"
        else:
            sample_rate = sr
            audio = generate_audio_buffer(sample_rate)

        ss = s.second * sample_rate
        ee = e.second * sample_rate

        print('  -', i, t)
        audio[ss:ss + len(data)] = data[0:]

    print()
    writewav(outputfile, sample_rate, audio)
    print('Done')

    try:
        os.remove(buffer_file)
    except:
        pass
        

def get_voices():
    engine = pyttsx3.init()
    return engine.getProperty('voices') 


def show_voice(i, v):
    print(f'  --- {i}')
    print('        Name', v.name)
    print('         Age', v.age, '\tGender', v.gender)
    print('   Languages', v.languages)


def select_voice(voices):
    engine = pyttsx3.init()

    for i, v in enumerate(voices):
        show_voice(i, v)
        print()

        engine.setProperty('voice', v.id)
        engine.say("I will speak this text")
        engine.runAndWait()

    return 0


def main():
    import argparse 

    default_file = 'E:/work/SubtitleToAudio/examples/captions.srt'

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=None, help='subtitle file to turn into audio')
    parser.add_argument('--voice', type=int, default=None, help='Voice index to use to generate audio')
    parser.add_argument('--output', type=str, default=None, help='Output folder')
    args = parser.parse_args()

    voices = get_voices()

    if args.voice is None:
        print('Select a Voice:')
        args.voice = select_voice(voices)
        print()
    else:
        print('Selected Voice:')
        show_voice(args.voice, voices[args.voice])
        print()

    filename = args.file or default_file
    outputfile = os.path.basename(filename) + '.wav'

    if args.output:
        outputfile = os.path.join(args.output, outputfile)
    
    read(filename, voices[args.voice].id, outputfile)


if __name__ == '__main__':
    main()
