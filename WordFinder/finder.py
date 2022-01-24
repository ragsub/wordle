from Wordle.settings import BASE_DIR
import json, os

letter1 = 'b'
letter2 = 'e'
letter3 = ''
letter4 = ''
letter5 = ''

letters_in = 'ad'

letters_not_in = 'rtyosnm'

five_letter_words = os.path.join(BASE_DIR, 'static', '5-letter-words.json')
en_dict = json.load(open(five_letter_words))
en_list = [en['word'] for en in en_dict]

print(en_list)