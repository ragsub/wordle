from Wordle.settings import BASE_DIR
import json, os

letter1 = ''
letter2 = ''
letter3 = ''
letter4 = ''
letter5 = ''

letters_in = 'on'

letters_not_in = 'ertiasfghm'

five_letter_words = os.path.join(BASE_DIR, 'static', '5-letter-words.json')
en_dict = json.load(open(five_letter_words))
en_list = [en['word'] for en in en_dict]

print(en_list)