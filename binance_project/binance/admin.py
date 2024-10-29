from django.contrib import admin
from .models import Pairs, PairsKlines


admin.site.register(Pairs)
admin.site.register(PairsKlines)
