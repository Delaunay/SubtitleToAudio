
import pyttsx3
from pysubparser import parser
from pysubparser.cleaners import ascii, brackets, formatting, lower_case


def test_text_to_speech():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 


    print(dir(voices[0]))
    for i, v in enumerate(voices):
        print(f'--- {i}')
        print('Age', v.age)
        print('Gender', v.gender)
        print('ID', v.id)
        print('Languages', v.languages)
        print('Name', v.name)

    print(len(voices))


    for i, v in enumerate(voices):
        engine.setProperty('voice', v.id)
        engine.say("I will speak this text")
        engine.runAndWait()


def readsubtitles(filename):

    def to_ascii(txt):
        return txt.encode('utf-8').decode("ascii","ignore")

    subtitles = formatting.clean(ascii.clean(brackets.clean(
        lower_case.clean(
            parser.parse(filename)
        )
    )))

    for subtitle in subtitles:
        yield subtitle.start, subtitle.end, to_ascii(subtitle.text), 


def read(filename):
    engine = pyttsx3.init()

    for i, (s, e, text) in enumerate(readsubtitles(filename)):

        #engine.say(text)
        print(text)
        engine.save_to_file(text , 'test.mp3')
        engine.runAndWait()

        if i > 2:
            break


if __name__ == '__main__':
    filename = 'E:/work/SubtitleToAudio/examples/example.srt'
    read(filename)
