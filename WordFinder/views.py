from django.shortcuts import render
import os, json

from Wordle.settings import BASE_DIR

# Create your views here.
def find_word(request):
    context={}

    exact = ' a   '
    letters_in = 'tka'

    letters_not_in = 'eryuiopsfhlcnm'

    five_letter_words = os.path.join(BASE_DIR, 'static', '5-letter-words.json')
    en_dict = json.load(open(five_letter_words))
    en_list = [en['word'] for en in en_dict]

    in_list = [char for char in letters_in]
    out_list = [char for char in letters_not_in]
    exact_list = [char for char in exact]

    target_list = []
    for word in en_list:
        out_list_flag = False
        in_list_flag = False
        exact_flag = False

        word_list = [char for char in word]
        for l in range(0,5):
            if (exact[l]!=' ') and (exact[l]!=word[l]):
                exact_flag=True
                continue
        
        if exact_flag==True:
            continue

        for l in in_list:
            if l not in word_list:
                in_list_flag = True
                continue
        
        if in_list_flag == True:
            continue

        for l in out_list:
            if l in word_list:
                out_list_flag = True
                continue
        if out_list_flag == True:
            continue
        
        target_list.append(word)

    print(target_list)
    return render(request=request, template_name='wordfinder/search.html', context=context)