from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CategorySexs(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20, choices=CategorySexs.choices, default=CategorySexs.OTHER
    )

    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="pets"
    )

    traits = models.ManyToManyField("traits.Trait", related_name="pets")
