from rest_framework import serializers
from api.models import Deal

class TopClientSerializer(serializers.Serializer):
    username = serializers.CharField(source='customer')
    spent_money = serializers.DecimalField(max_digits=10, decimal_places=2)
    gems = serializers.SerializerMethodField()

    def get_gems(self, obj):
        gem_list = self.context.get('gem_list', [])
        return gem_list

    class Meta:
        fields = ('username', 'spent_money', 'gems')
