from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class OwnedObjectModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class CertificationAuthority(OwnedObjectModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2048)

    def __str__(self):
        return self.name


class CACertificate(OwnedObjectModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2048)
    certification_authority = models.ForeignKey(CertificationAuthority, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
