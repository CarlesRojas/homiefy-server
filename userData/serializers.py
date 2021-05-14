from rest_framework import serializers



class debtResposeSerializer(serializers.Serializer):
    """
        Serializer for the debt End point
    """
    username = serializers.CharField(required=True)
    totalDebt = serializers.IntegerField(required=True)
    subDebt = serializers.DictField(required=True)