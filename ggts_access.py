from googletrans import Translator
from gtts import gTTS


def download_mp3(word, lang):
    tts = gTTS(word, lang=lang)
    tts.save('{}.mp3'.format(word))


def translate_file(file, src_lng, dst_lng):
    # open file
    f = open(file, 'r')
    line_lst = f.read().splitlines()
    line_lst_filter = filter(None, line_lst)

    # download mp3 (retry if fetch failed)
    for word in line_lst_filter:
        while True:
            try:
                print(word)
                download_mp3(word, src_lng)
            except Exception as exp:
                print(exp)
                continue
            break

    # translate
    translator = Translator()
    translation_lst = []
    line_lst_filter = filter(None, line_lst)
    for word in line_lst_filter:
        if word is None:
            continue
        translation = translator.translate(word, src=src_lng, dest=dst_lng)
        translation_lst.append(translation.text)

    return translation_lst


with open('result.txt', 'w') as file_handle:
    for item in translate_file('vocab.txt', 'it', 'en'):
        file_handle.write('%s\n' % item)
