""" Testing Views module of DOPIGO Challenge / Banking API """
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory,TestCase
from django.urls import reverse

from api.models import Account, Action, Customer
from api.views import AccountViewSet, AccountViewSet, \
    ActionViewSet, BalanceViewSet, MoneyTransferViewSet

class AccountTestCase(TestCase):
    """ Test module of POST create-account """
    def setUp(self):
        # Access to the request factory
        self.factory = RequestFactory()
        # Create customer DB
        Customer.objects.create(id=1, name="Arisha Barron")
        Customer.objects.create(id=2, name="Branden Gibson")
        Customer.objects.create(id=3, name="Rhonda Church")
        Customer.objects.create(id=4, name="Georgina Hazel")

    def test_customer_create_account(self):
        # Create an instance of POST - create account
        request = self.factory.post('/create-account/', 
            data={'holder': 'Arisha Barron',
                  'balance': '1000',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing AccountViewSet 
        response = AccountViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)

    def test_customer_create_another_account(self):
        # Create the first account of customer
        request = self.factory.post('/create-account/', 
            data={'holder': 'Arisha Barron',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)

        # Create an instance of POST - create account
        request = self.factory.post('/create-account/', 
            data={'holder': 'Arisha Barron',
                  'balance': '1000',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing AccountViewSet 
        response = AccountViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)


    def test_invalid_customer_create_account(self):
        # Create an instance of POST - create account
        request = self.factory.post('/create-account/', 
            data={'holder': 'Michael Scott',
                  'balance': '10000',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing AccountViewSet 
        response = AccountViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

    def test_account_check_balance(self):
        # Create an account to check balance
        request = self.factory.post('/create-account/', 
            data={'holder': 'Arisha Barron',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)

        # Create an instance of GET - checking balance
        request = self.factory.get('/check-balance/', 
            data={'account_id': '1',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing BalanceViewSet 
        response = BalanceViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)    

    def test_invalid_account_check_balance(self):
        # Create an instance of GET - checking balance
        request = self.factory.get('/check-balance/',
            data={'account_id': '1',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing BalanceViewSet 
        response = BalanceViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 400)

    def test_account_create_money_transfer(self):
        # Create account for sender
        request = self.factory.post('/create-account/', 
            data={'holder': 'Arisha Barron',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)  

        # Create an account for receiver
        request = self.factory.post('/create-account/', 
            data={'holder': 'Branden Gibson',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)  
        # Create an instance of POST - create money transfer
        request = self.factory.post('/create-transfer/', 
            data={'sender': '1',
                  'receiver': '2',
                  'amount': '500',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing MoneyTransferViewSet 
        response = MoneyTransferViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)

    def test_same_customer_create_money_transfer(self):
        """ Same customer, different accounts situation """
        # Create account for sender 
        request = self.factory.post('/create-account/', 
            data={'holder': 'Arisha Barron',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)  

        # Create an account for receiver
        request = self.factory.post('/create-account/', 
            data={'holder': 'Arisha Barron',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)  
        # Create an instance of POST - create money transfer
        request = self.factory.post('/create-transfer/', 
            data={'sender': '1',
                  'receiver': '2',
                  'amount': '500',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing MoneyTransferViewSet 
        response = MoneyTransferViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)

    def test_insufficient_funds_create_money_transfer(self):
        # Create account for sender 
        request = self.factory.post('/create-account/', 
            data={'holder': 'Arisha Barron',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)  

        # Create an account for receiver
        request = self.factory.post('/create-account/', 
            data={'holder': 'Branden Gibson',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)  
        # Create an instance of POST - create money transfer
        request = self.factory.post('/create-transfer/', 
            data={'sender': '1',
                  'receiver': '2',
                  'amount': '1500',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing MoneyTransferViewSet 
        response = MoneyTransferViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_amount_create_money_transfer(self):
        # Create account for sender 
        request = self.factory.post('/create-account/', 
            data={'holder': 'Arisha Barron',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)  

        # Create an account for receiver
        request = self.factory.post('/create-account/', 
            data={'holder': 'Branden Gibson',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)  
        # Create an instance of POST - create money transfer
        request = self.factory.post('/create-transfer/', 
            data={'sender': '1',
                  'receiver': '2',
                  'amount': '-1500',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing MoneyTransferViewSet 
        response = MoneyTransferViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_sender_create_money_transfer(self):
        # Create account for receiver 
        request = self.factory.post('/create-account/', 
            data={'holder': 'Arisha Barron',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)  

        # Create an instance of POST - create money transfer
        request = self.factory.post('/create-transfer/', 
            data={'sender': '2',
                  'receiver': '1',
                  'amount': '500',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing MoneyTransferViewSet 
        response = MoneyTransferViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_receiver_create_money_transfer(self):
        # Create account for sender 
        request = self.factory.post('/create-account/', 
            data={'holder': 'Arisha Barron',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)  

        # Create an instance of POST - create money transfer
        request = self.factory.post('/create-transfer/', 
            data={'sender': '1',
                  'receiver': '2',
                  'amount': '500',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing MoneyTransferViewSet 
        response = MoneyTransferViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

    def test_same_customer_create_money_transfer(self):
        """ Same customer, same account situation """
        # Create account for sender and receiver
        request = self.factory.post('/create-account/', 
            data={'holder': 'Arisha Barron',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)  
        # Create an instance of POST - create money transfer
        request = self.factory.post('/create-transfer/', 
            data={'sender': '1',
                  'receiver': '1',
                  'amount': '500',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing MoneyTransferViewSet 
        response = MoneyTransferViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

    def test_account_retreive_action(self):
        # Create account for sender
        request = self.factory.post('/create-account/', 
            data={'holder': 'Arisha Barron',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)  

        # Create an account for receiver
        request = self.factory.post('/create-account/', 
            data={'holder': 'Branden Gibson',
                  'balance': '1000',
                  })
        
        request.user = AnonymousUser()
        response = AccountViewSet.as_view({'post': 'create'})(request)  

        # Create an action as sender
        request = self.factory.post('/create-transfer/', 
            data={'sender': '1',
                  'receiver': '2',
                  'amount': '500',
                  })
        
        request.user = AnonymousUser()
        response = MoneyTransferViewSet.as_view({'post': 'create'})(request)

        # Create an action as receiver
        request = self.factory.post('/create-transfer/', 
            data={'sender': '1',
                  'receiver': '2',
                  'amount': '500',
                  })
        
        request.user = AnonymousUser()
        response = MoneyTransferViewSet.as_view({'post': 'create'})(request)

        # Create a GET request to retreive transfer history
        request = self.factory.get('/retrieve-action/', 
            data={'account_id': '1',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing ActionViewSet 
        response = ActionViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_invalid_account_retreive_action(self):
        # Create a GET request to retreive transfer history
        # without creating any accounts 
        
        request = self.factory.get('/retrieve-action/', 
            data={'account_id': '3',
                  })
        
        # Create an anonymous user 
        request.user = AnonymousUser()

        # Testing ActionViewSet 
        response = ActionViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 400)





