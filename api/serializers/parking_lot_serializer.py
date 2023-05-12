from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer, ModelSerializer
from webapp.models.parking_lot import ParkingLot, LotImage


class LotImageSerializer(ModelSerializer):
    class Meta:
        model = LotImage
        fields = ("image",)


class ParkingLotSerializer(GeoModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    images = serializers.SerializerMethodField()
    # distance = serializers.SerializerMethodField()

    class Meta:
        model = ParkingLot
        fields = "__all__"
        geo_field = 'location'

    def create(self, validated_data):
        images = self.context['images']
        lot = ParkingLot.objects.create(
            owner=self.context['request'].user,
            **validated_data
        )
        for image in images:
            LotImage.objects.create(lot=lot,
                                    image=image)
        return lot

    def get_images(self, obj):
        imagesSerializer = LotImageSerializer(LotImage.objects.filter(lot=obj), many=True)
        return [data['image'] for data in imagesSerializer.data]

    # def get_distance(self, obj):
    #     location = self.context.get('location', None)
    #     if location:
    #         return obj.location.distance(location)
    #     else:
    #         return None
