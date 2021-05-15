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
    price           = serializers.DecimalField(max_digits=20, decimal_places=5,      help_text="price of the utility")
    people          = serializers.ListField(required=True,     help_text="people that uses that utility")
    period          = serializers.IntegerField(required=True,     help_text="days of the utility period")
    lastPayment     = serializers.CharField(required=True,help_text="date of the last payment")
    picture         = serializers.CharField(required=True,help_text="icon of the utility")


class UtilityDictSerializer(serializers.Serializer):
    response = serializers.DictField(child = UtilitySerializer())


class UtilitySelectorSerializer(serializers.Serializer):
    """
        Serializer for the new utility.
    """
    username        =serializers.CharField(required=True, help_text="user that pays the utility")
    name            = serializers.CharField(required=True,       help_text="name of the utility")



class newExpenseSerializer(serializers.Serializer):
    """
        Adds a expense to the users balance.
    """
    username        =serializers.CharField(required=True, help_text="user that pays the utility")
    people          = serializers.ListField(required=True,     help_text="people that uses that is involved in the expense")
    price           = serializers.DecimalField(max_digits=20, decimal_places=5,      help_text="price of the expense")
    name            = serializers.CharField(required=False,       help_text="name of the utility")


class ExpenseSelectorSerializer(serializers.Serializer):
    """
        Serializer for the new Expense.
    """
    username        =serializers.CharField(required=True, help_text="user that pays the utility")
