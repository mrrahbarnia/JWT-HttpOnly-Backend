from django.db.models import QuerySet

from transactions.models import Transaction

def list_transactions() -> QuerySet[Transaction]:
    q =  Transaction.objects.only('id', 'amount')
    return q