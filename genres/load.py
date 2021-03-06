import os
import csv
from django.utils.text import slugify

from .models import Category, Genre
from annoying.functions import get_object_or_None


genre_csv = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           'data/genres.txt'))
categories_csv = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           'data/categories.txt'))

def run(verbose=True):

    for row in csv.reader(open(categories_csv),delimiter=','):
        name = row.pop(0).strip()
        popular = row.pop(0).strip()
        slug = slugify(unicode(name))
        category, created = Category.objects.get_or_create(name=name, slug=slug)
        if popular == "True":
            category.popular = True
        else:
            category.popular = False

        category.save()

    for row in csv.reader(open(genre_csv),delimiter=','):
        # remove and save the first element in the list
        # .strip() romoves leading & trailing spaces
        genre_name = row.pop(0).strip()
        genre = get_object_or_None(Genre, name=genre_name)
        if not genre:
            try:
                genre_slug = slugify(unicode(genre_name))
                genre = Genre.objects.create(name=genre_name,slug=genre_slug)
            except:
                #print name to bo corrected
                print genre_name
        for category_name in row:
            category_name = category_name.strip()
            category = get_object_or_None(Category, name=category_name)
            if category:
                category.genres.add(genre)
                category.save()
            else:
                print "category: " + category_name + " was not found"
