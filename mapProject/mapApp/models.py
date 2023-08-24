from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    emailConfirmed = models.BooleanField(default=False)

    def get_admin_user(self):
        return User.objects.filter(is_superuser=True).first()


# Osm_id is unique only within object type
# http://www.openstreetmap.org/way/40000000 vs http://www.openstreetmap.org/node/40000000
# Number of nodes     2412050198
# Number of ways      241029453
# Number of relations 2658037
# Every OSM object follows this coding scheme in order ==> typeObject + Id + Version(?)
# > Type of object (node/way/relation)
# > Id
# > Version of object

# https://www.openstreetmap.org/node/805825943
# https://www.openstreetmap.org/[typeOSM]/[osmID]

# https://nominatim.openstreetmap.org/search.php?q=490%20rue%20des%20croisades&polygon_geojson=1&format=jsonv2


class Property(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    place_id = models.IntegerField(null=False, blank=False)
    osm_id = models.IntegerField(null=False, blank=False)
    osm_type = models.CharField(null=False, blank=False, max_length=20)
    lat = models.DecimalField(max_digits=20, decimal_places=15)
    lon = models.DecimalField(max_digits=20, decimal_places=15)
    display_name = models.CharField(null=False, blank=False, max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name


class Project(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="projectFromProperty")
    title = models.CharField(null=False, blank=False, max_length=255)
    description = models.CharField(null=True, blank=True, max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Choice(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    description = models.CharField(null=False, blank=False, max_length=500)
    order = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.description