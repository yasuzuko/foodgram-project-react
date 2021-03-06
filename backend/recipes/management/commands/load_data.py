import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузить таблицу ингридиентов в БД'

    def handle(self, *args, **options):
        id = 0
        with open('recipes/data/ingredients.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            for line in reader:
                name, unit = line
                Ingredient.objects.get_or_create(
                    id=id,
                    name=name,
                    measurement_unit=unit
                    )
                id += 1
