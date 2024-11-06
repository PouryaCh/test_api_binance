from django.contrib import admin
from .models import Exchange, Pairs, PairsKlines


admin.site.register(Pairs)
admin.site.register(PairsKlines)
admin.site.register(Exchange)
