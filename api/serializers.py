""" Serializers module of DOPIGO Challenge / Banking API """
from django.db import transaction
from rest_framework import serializers

from .models import Account, Action, Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name']

class AccountSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Account
        fields = ['id', 'holder', 'balance']

class AccountBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'balance']

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'created', 'sender', 'receiver', 'amount']

class MoneyTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['sender', 'receiver', 'amount']

    def create(self, data):
        """ This method creates an action solely transfers money \
        from one account to another. Action is limited to \
        money transfer but it can be extendable when in need. """

        with transaction.atomic():

            if data['sender'] == data['receiver']:
                raise serializers.ValidationError({
                'receiver': 'can not be sender!'
            })

            amount = data['amount']

            if amount < 1:
                raise serializers.ValidationError({
                'amount': 'can not be below 1!'
            })            

            try:
                sender = Account.objects.select_for_update().get(
                    pk=data['sender'].pk
                    )
            except Account.DoesNotExist:
                raise serializers.ValidationError({
                    'sender': 'Invalid account number!'
            })

            try:
                receiver = Account.objects.select_for_update().get(
                    pk=data['receiver'].pk
                    )
            except Account.DoesNotExist:
                raise serializers.ValidationError({
                    'receiver': 'Invalid account number!'
            })          

            if sender.balance - amount < 0:
                raise serializers.ValidationError({
                    'amount': 'Insufficient funds!'
            })
            sender.balance -= amount
            sender.save(update_fields=[
                'balance',
            ])
            receiver.balance += amount
            receiver.save(update_fields=[
                'balance',
            ])

            action = Action.objects.create(
                sender=sender,
                receiver=receiver,
                amount=amount,
            )
        
        return action


