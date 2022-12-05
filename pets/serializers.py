from rest_framework import serializers
from .models import Pet, CategorySexs
from groups.serializers import GroupSerializer
from groups.models import Group
from traits.models import Trait
from traits.serializers import TraitSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=CategorySexs.choices,
        default=CategorySexs.OTHER,
    )
    traits_count = serializers.SerializerMethodField()

    group = GroupSerializer()

    traits = TraitSerializer(many=True)

    def get_traits_count(self, obj: Pet):
        trait_list = Pet.objects.get(id=obj.id).traits.all()

        result = len(trait_list)

        return result

    def create(self, validated_data):
        traits_list = validated_data.pop("traits")
        group_obj = validated_data.pop("group")

        group_dict, created = Group.objects.get_or_create(**group_obj)

        pet = Pet.objects.create(**validated_data, group=group_dict)

        for trait_dict in traits_list:
            trait, created = Trait.objects.get_or_create(**trait_dict)

            pet.traits.add(trait)

        return pet

    def update(self, instance, validated_data):
        traits = validated_data.pop("traits", None)
        groups = validated_data.pop("group", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if groups:
            group, created = Group.objects.get_or_create(**groups)

            for key, value in groups.items():
                setattr(group, key, value)

            group.save()

        if traits:
            instance.traits.clear()

            for trait in traits:
                trait_obj, created = Trait.objects.get_or_create(**trait)
                instance.traits.add(trait_obj)

            instance.save()

        return instance
