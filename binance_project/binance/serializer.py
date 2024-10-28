# from rest_framework import serializers
# from .models import BinancePair

# class BinancePairSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = BinancePair
#         fields = ['symbol', 'price', 'timestamp']


from rest_framework import serializers
from .models import Pairs

class PairsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pairs
        fields = '__all__'