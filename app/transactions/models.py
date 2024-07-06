from django.db import models

from common.models import BaseModel


class Transaction(BaseModel):
    amount = models.FloatField()

    def __str__(self) -> str:
        return f'{self.pk} >> {self.amount}'