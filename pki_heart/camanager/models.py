from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class OwnedObjectModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CertificationAuthority(OwnedObjectModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=2048)

    def __str__(self):
        return self.name

    def clean(self):
        if self.name:
            self.name = self.name.strip()


class CACertificate(OwnedObjectModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=2048)
    certification_authority = models.ForeignKey(CertificationAuthority, on_delete=models.CASCADE)
    issued_by_certificate = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True)
    # if True then this certificate can issue other client certificates
    allow_issue = models.BooleanField(default=False)
    # complete string representation of X.509 Subject
    subject = models.CharField(max_length=1024)
    # see pk_heart.utils.supported_private_key_algorithms()
    private_key_algorithm = models.CharField(max_length=100)
    # ENCRYPTED private key
    private_key = models.BinaryField(max_length=1024*4, default=b'')
    # X.509 certificate in DER format
    certificate = models.BinaryField(max_length=1024*50, default=b'')

    def __str__(self):
        return self.name

    def clean(self):
        if self.name:
            self.name = self.name.strip()
