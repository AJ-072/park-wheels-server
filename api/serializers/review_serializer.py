from rest_framework import serializers

from webapp.models import Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class ReviewWithUserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'

    def get_username(self, obj):
        return obj.booking.user.username
