from django.contrib import admin
from .models import Transaction, TransactionReason, TransactionDetails, ParentContainerArrears

admin.site.register(TransactionDetails)

admin.site.register(Transaction)
admin.site.register(TransactionReason)
admin.site.register(ParentContainerArrears)
# Register your models here.
