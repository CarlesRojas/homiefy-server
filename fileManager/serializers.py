from rest_framework import serializers


class profilePicSerializer(serializers.Serializer):
    """
        Serializer for the profile pic.
    """
    username        =serializers.CharField(required=True, help_text="user that pays the utility")