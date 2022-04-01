from django.db import models

from associations.validators import validate_country_name
from banks.models import Bank
from programs.models import Program


class Association(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE,)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE,)
    country = models.TextField(null=False, validators=[validate_country_name])

    def __str__(self):
        return f"{self.program} {self.bank} {self.country}"

    class Meta:
        unique_together = ("program", "bank", "country")
