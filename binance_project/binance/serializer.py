# from rest_framework import serializers
# from .models import BinancePair

# class BinancePairSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = BinancePair
#         fields = ['symbol', 'price', 'timestamp']


from rest_framework import serializers
from .models import Exchange, Pairs, PairsKlines



class ExchangeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Exchange
        fields = '__all__'





class PairsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pairs
        fields = '__all__'
        
                
        
 
class KlineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PairsKlines
        fields = '__all__'