
from rest_framework import serializers

class WinnerSerializer(serializers.Serializer):
    contest_title = serializers.CharField(max_length=255)
    contest_description = serializers.CharField(max_length=255)
    contest_end_date = serializers.DateTimeField()
    winner_name = serializers.CharField(max_length=255)
    winning_photo = serializers.ImageField()
