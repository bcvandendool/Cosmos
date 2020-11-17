import math

from django.contrib.auth.models import Group
from django.core.validators import ValidationError
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField
from djangocms_text_ckeditor.fields import HTMLField

# The board model is defined here


def validate_aspect_ratio(image):
    # Function used to check if the board picture uses the correct aspect ratio
    ratio = 1.5
    if not math.isclose(image.width / image.height, ratio, rel_tol=1e-6):
        raise ValidationError("The aspect ratio is not correct. The aspect ratio should be: " + str(ratio))


class Board(models.Model):

    # Extension of Django Group modelt to store extra data of the board.

    # - `name`, `permissions`: self-explanatory

    # To get all groups of a user you can do this:

    # - user.groups.all()

    # To get all users of a group:

    # - group.user_set.all()

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    description = HTMLField(blank=True)
    period_from = models.DateField(blank=False)
    period_to = models.DateField()
    pretix_organizer_token = models.CharField(max_length=20, blank=True)
    members = ArrayField(models.CharField(max_length=100, blank=True), blank=True, default=list)
    display_name = models.CharField(max_length=50, blank=False, default="None")
    slug = models.CharField(max_length=20, blank=False, default="None")

    photo = models.ImageField(
        upload_to="boards",
        default="boards/default.jpg",
        validators=[validate_aspect_ratio],
    )

    # @property is used to return the output of a function as type of variable so it can be used in the template
    # https://docs.python.org/3/library/functions.html#property
    @property
    def name(self):
        return self.group.name

    # @property is used to return the output of a function as type of variable so it can be used in the template
    # https://docs.python.org/3/library/functions.html#property
    @property
    def permissions(self):
        return self.group.permissions

    def __str__(self):
        return f"{self.name}: {self.description}"
