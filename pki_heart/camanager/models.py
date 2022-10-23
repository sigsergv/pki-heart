from django.db import models

class CertificationAuthority(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2048)

    def __str__(self):
        return self.name


class CACertificate(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2048)
    certification_authority = models.ForeignKey(CertificationAuthority, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
