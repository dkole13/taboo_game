from django.http import HttpResponse
from django.shortcuts import render
import random
from django.http import JsonResponse
from .models import Word


def start(request):
    return render(request, 'game/home.html')


def show_card(request):
    return render(request, 'game/start.html')


def get_random_word(request):
    used_ids = request.session.get('used_words', [])
    words = Word.objects.exclude(id__in=used_ids)

    if not words.exists():
        return JsonResponse({"word": None})

    word_obj = random.choice(list(words))

    used_ids.append(word_obj.id)
    request.session['used_words'] = used_ids

    result = {
        "id": word_obj.id,
        "word": word_obj.word,
        "taboo_words": [
            word_obj.taboo_word_1,
            word_obj.taboo_word_2,
            word_obj.taboo_word_3,
            word_obj.taboo_word_4,
            word_obj.taboo_word_5,
        ],
    }
    return JsonResponse(result)
