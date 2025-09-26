from rest_framework import serializers
from .models import Animal, MilkRecord

class AnimalSerializer(serializers.ModelSerializer):
    full_siblings = serializers.SerializerMethodField()
    half_siblings = serializers.SerializerMethodField()
    age_days = serializers.ReadOnlyField()

    class Meta:
        model = Animal
        fields = ["id","ear_tag","name","sex","breed","date_of_birth",
                  "sire","dam","is_alive","notes","age_days",
                  "full_siblings","half_siblings"]

    def get_full_siblings(self, obj):
        return list(obj.full_siblings().values("id","ear_tag","name"))

    def get_half_siblings(self, obj):
        return list(obj.half_siblings().values("id","ear_tag","name"))

class MilkRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkRecord
        fields = ["id","animal","date","liters","notes"]
