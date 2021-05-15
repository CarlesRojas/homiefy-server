from rest_framework import serializers



class debtResposeSerializer(serializers.Serializer):
    """
        Serializer for the debt End point
    """
    username = serializers.CharField(required=True)
    totalDebt = serializers.IntegerField(required=True)
    subDebt = serializers.DictField(required=True)



class UtilitySerializer(serializers.Serializer):
    """
        Serializer for the new utility.
    """
    username        =serializers.CharField(required=True, help_text="user that pays the utility")
    name            = serializers.CharField(required=False,       help_text="name of the utility")
    price           = serializers.IntegerField(required=True,      help_text="price of the utility")
    people          = serializers.ListField(required=True,     help_text="people that uses that utility")
    period          = serializers.IntegerField(required=True,     help_text="days of the utility period")
    lastPayment     = serializers.CharField(required=True,help_text="date of the last payment")


class UtilityDictSerializer(serializers.Serializer):
    response = serializers.DictField(child = UtilitySerializer())


class UtilitySelectorSerializer(serializers.Serializer):
    """
        Serializer for the new utility.
    """
    username        =serializers.CharField(required=True, help_text="user that pays the utility")
    name            = serializers.CharField(required=True,       help_text="name of the utility")
