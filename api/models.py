""" Models module of DOPIGO Challenge / Banking API """
from django.db import models

# Defining the customer/client 
class Customer(models.Model):
    """ Customer has two class variables: id and name. \
    Id is set manually, not auto-incremented """

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    id = models.IntegerField(
        primary_key=True
        )
    name = models.CharField(
        max_length=100
        )

# Defining the account
class Account(models.Model):
    """ Account has three variables: account id, total \
    balance and the owner/holder of the account """

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    id = models.AutoField(
        primary_key=True
        )
    holder = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
        )
    balance = models.DecimalField(
        max_digits=20, 
        decimal_places=2
        )


# Defining the transaction
class Action(models.Model):
    """ Action can be considered as an transaction model. \
    Here I am using action name to avoid clashes with \
    Django.DB.transaction module/instances... """

    class Meta:
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'

    id = models.AutoField(primary_key=True)

    created = models.DateTimeField(
        auto_now_add=True
        )
    sender = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='sender'
        )
    receiver = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='receiver'
        )
    amount = models.DecimalField(
        max_digits=20, 
        decimal_places=2
        )

        



