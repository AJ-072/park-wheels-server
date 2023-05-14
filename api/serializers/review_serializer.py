from rest_framework import serializers

from webapp.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        review = Review.objects.create(
            lot=self.context['lot_id'],
            user=self.context['user'],
            **validated_data
        )
        return review
