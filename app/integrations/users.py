from .models import ElinkStellarAccount, ElinkUser, ElinkUserKYC, ElinkPayment

# Create your views here.

def calculate_fee():
    return 3.45

def user_for_account(account_id):
    #to get the user account linked to a stellar public key
    
    print("user-for-account >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        
    try:
        stellar_account = ElinkStellarAccount.objects.filter(account=account_id)\
                            or ElinkStellarAccount.objects.filter(memo=account_id)

        print("count = ", stellar_account.count())

        if stellar_account.count() == 1:
            print('stellar account => ', stellar_account.values()[0])
            print('user => ', ElinkUser.objects.get(id=stellar_account.values()[0].get('user_id')))
            return ElinkUser.objects.get(id=stellar_account.values()[0].get('user_id'))

        return None
    except:
        print('Error')
        return None

def user_for_id(account_id):
    #to get the user account linked to a stellar public key
    
    try:
        stellar_account = ElinkStellarAccount.objects.filter(account=account_id)\
                            or ElinkStellarAccount.objects.filter(memo=account_id)

        if stellar_account.count() == 1:
            print('stellar account => ', stellar_account.values()[0])
            print('user => ', ElinkUser.objects.get(id=stellar_account.values()[0].get('user_id')))
            return ElinkUser.objects.get(id=stellar_account.values()[0].get('user_id'))

        return None
    except:
        print('Error')
        return None

def verify_bank_account(routing_number, account_number):
    
    return True
    # try:
    #     stellar_account = AppStellarAccount.objects.filter(account=account_id)\
    #                         or AppStellarAccount.objects.filter(memo=account_id)

    #     if stellar_account.count() == 1:
    #         return stellar_account.values()[0]

    #     return None
    # except:
    #     print('Error')
    #     return None

def save_customer(account, params):
    try:
        uid = ElinkUser.objects.latest('id').id
        if uid == None:
            uid = 0
        user = ElinkUser.objects.create(
            id=uid + 1,
            first_name=params.get('first_name'),
            last_name=params.get('last_name'),
            email=params.get('email_address'),
            phone_number="",
            address=params.get(''),
            bank_account_number=params.get('bank_account_number'),
            bank_number=params.get('bank_number')
        )
        
        print('uid=', uid+1)

        accId = ElinkStellarAccount.objects.latest('id').id
        if accId == None:
            accId = 0

        print('accId=', accId+1)

        return ElinkStellarAccount.objects.create(
            user=user,
            id=accId + 1,
            memo = params.get('memo'),
            memo_type = params.get('memo_type'),
            account = account,
            muxed_account = account,
            secret_key = "",
            confirmed = True,
            confirmation_token = "",
            user_id=uid+1,
        )
    except:
        return None

def fields_for_type(type):
    return {
        "bank_account_number": {
            "description": "bank account number of the customer",
            "type": "string"
        },
        "bank_number": {
            "description": "routing number of the customer",
            "type": "string"
        },
        "email_address": {
            "description": "email address of the customer",
            "type": "string"
        },
        "first_name": {
            "description": "first name of the customer",
            "type": "string",
        },
        "last_name": {
            "description": "last name of the customer",
            "type": "string"
        },
        "photo_id_back": {
            "description": "Image of back of user's photo ID or passport",
            "optional": True,
            "type": "binary"
        },
        "photo_id_front": {
            "description": "Image of front of user's photo ID or passport",
            "optional": True,
            "type": "binary"
        }
    }