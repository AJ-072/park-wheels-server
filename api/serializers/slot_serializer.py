from rest_framework import serializers
from webapp.models import Slot
from rest_framework.validators import UniqueValidator


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = "__all__"


class SlotIdSerializer(serializers.ModelSerializer):
    slot_id = serializers.IntegerField(required=True, source='id')

    class Meta:
        model = Slot
        fields = "__all__"
        read_only_fields = "__all__"

    def validate_id(self, value):
        try:
            obj = self.Meta.model.objects.get(id=value)
        except self.Meta.model.DoesNotExist:
            raise serializers.ValidationError('Object with this ID does not exist')
        return value
