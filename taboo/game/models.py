from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=255, db_index=True)
    taboo_word_1 = models.CharField(max_length=255, default='')
    taboo_word_2 = models.CharField(max_length=255, default='')
    taboo_word_3 = models.CharField(max_length=255, default='')
    taboo_word_4 = models.CharField(max_length=255, default='')
    taboo_word_5 = models.CharField(max_length=255, default='')
