import os, json, random
from cryptography.fernet import Fernet

from django.shortcuts import render
from django.forms.formsets import formset_factory
from django.contrib import messages

from Wordle.settings import BASE_DIR
from Word.forms import WordleForm, GuessForm, AlphabetForm

ENCODING_FORMAT='utf8'

def process_word(request):

    #load the 5-words scrabble dictionary
    five_letter_words = os.path.join(BASE_DIR, 'static', '5-letter-words.json')
    en_dict = json.load(open(five_letter_words))
    en_list = [en['word'] for en in en_dict]

    #initiate cryptography
    SECRET_KEY = bytes(os.getenv('ENCRYPTION_KEY', None),ENCODING_FORMAT)
    f = Fernet(SECRET_KEY)

    #initiate array for alphabet colors
    AlphabetFormSet = formset_factory(AlphabetForm, extra=26, max_num=26)
    
    #initiate formset for guesslist
    GuessFormSet = formset_factory(GuessForm, extra=6, max_num=6)

    #initialize context
    context = {}

    if request.method == 'POST':
        #read the forms from copy of request.POST to make them mutable
        guess_formset = GuessFormSet(request.POST.copy(), form_kwargs={'empty_permitted': False}, prefix='guess')
        alphabet_formset = AlphabetFormSet(request.POST.copy(), form_kwargs={'empty_permitted': False}, prefix='alphabet')
        form = WordleForm(request.POST.copy())

        if guess_formset.is_valid() & form.is_valid() & alphabet_formset.is_valid():
            #get the target word and decrypt
            TARGET_WORD = f.decrypt(bytes(form.cleaned_data['target_word'],ENCODING_FORMAT)).decode()
            #get the other form data
            guess = form.cleaned_data['guess'].lower()
            attempts_left = form.cleaned_data['attempts_left']
            print(attempts_left)    
            attempt_number = form.cleaned_data['attempt_number']
            
            #clear the word for the next refresh
            form.data['word'] = ""

            #check sufficient attempts are left
            if attempts_left > 0:
                #check if entered word is in dictionary
                if guess in en_list:
                    #valid attempt to increment
                    form.data['attempt_number'] = attempt_number+ 1
                    form.data['attempts_left'] = attempts_left - 1

                    #get the latest word
                    guess_form = guess_formset[attempt_number-1]
                    guess_form.cleaned_data['guess'] = guess
                    #go through each word
                    for j in range(0,5):
                        letter_color = 'l'+str(j+1)+'_color'
                        if guess[j] == TARGET_WORD[j]:
                            guess_form.cleaned_data[letter_color] = 'bg-success'
                            alphabet_formset[ord(guess[j])-97].cleaned_data['l_color'] = 'btn-success'
                        elif guess[j] in TARGET_WORD:
                            guess_form.cleaned_data[letter_color] = 'bg-warning'
                            if alphabet_formset[ord(guess[j])-97].cleaned_data['l_color'] != 'btn-success':
                                alphabet_formset[ord(guess[j])-97].cleaned_data['l_color'] = 'btn-warning'
                        else:
                            guess_form.cleaned_data[letter_color] = 'bg-secondary'
                            alphabet_formset[ord(guess[j])-97].cleaned_data['l_color'] = 'btn-secondary'
                    
                    new_guess_formset = GuessFormSet(initial = guess_formset.cleaned_data, prefix='guess')
                    new_alphabet_formset = AlphabetFormSet(initial = alphabet_formset.cleaned_data,prefix='alphabet')

                    context['form'] = form
                    context['guess_formset'] = new_guess_formset
                    context['alphabet_formset'] = new_alphabet_formset

                    if guess == TARGET_WORD:
                        messages.add_message(request=request, level=messages.SUCCESS, message='You solved it in '+ str(attempt_number) + ' attempts! Challenge your friend by clicking '+'<a href='+request.path+'?target_word='+form.cleaned_data['target_word']+'>here</a>', extra_tags='safe')

                    if attempts_left == 1:
                        messages.add_message(request=request, level=messages.ERROR, message = 'Chances over. word is '+TARGET_WORD)

                else:
                    messages.add_message(request=request, level=messages.ERROR, message=guess+' is not a valid english word')
                    context['guess_formset'] = guess_formset
                    context['form'] = form
                    context['alphabet_formset'] = alphabet_formset

            else:
                messages.add_message(request=request, level=messages.ERROR, message = 'Chances over. word is '+TARGET_WORD)
                context['guess_formset'] = guess_formset
                context['form'] = form
                context['alphabet_formset'] = alphabet_formset


        else:
            print(form.errors)
            print(form.non_field_errors)
            print(guess_formset.errors)
            print(guess_formset.non_form_errors())
            print(alphabet_formset.errors)
            print(alphabet_formset.non_form_errors())
    else:
        #initiate the forms
        form = WordleForm()
        form.fields['attempts_left'].initial= 6
        form.fields['attempt_number'].initial = 1
        guess_formset = GuessFormSet(prefix='guess')
        alphabet_formset = AlphabetFormSet(prefix='alphabet')
        i=1
        for guess_form in guess_formset:
            x_ref = 'guess_'+str(i)
            guess_form.fields['guess'].widget.attrs.update({'x-ref':x_ref,'x-model':x_ref+'_xmodel'})
            i=i+1

        #see if the word is in the link, else get a new word encrypt and store in form
        if request.GET.get('target_word',None) == None:
            target_word = random.choice(en_list)
            encrypted_word = f.encrypt(bytes(target_word, ENCODING_FORMAT))
            form.fields['target_word'].initial = encrypted_word.decode()
        else:
            request.GET._mutable = True
            encrypted_word = request.GET.get('target_word')
            form.fields['target_word'].initial = encrypted_word
            request.GET['target_word'] = None

        #initiate the variables to send to the template
        context['form'] = form
        context['guess_formset'] = guess_formset
        context['alphabet_formset'] = alphabet_formset

    #send back the html template
    return render(request=request, template_name='word/index1.html', context=context)


def help_menu(request):
    pass