from typing import Dict, List
from polaris.integrations import WithdrawalIntegration
from polaris.sep10.token import SEP10Token
from polaris.models import Transaction
from rest_framework.request import Request
from .users import user_for_account#, calculate_fee
# from .rails import calculate_fee, memo_for_transaction

class AnchorWithdrawSep6(WithdrawalIntegration):
    def process_sep6_request(
        self,
        token: SEP10Token,
        request: Request,
        params: Dict,
        transaction: Transaction,
        *args: List,
        **kwargs: Dict
    ) -> Dict:
        # check if the user's KYC has been approved
        kyc_fields = [
            "first_name",
            "last_name",
            "email_address",
            "address",
            "bank_account_number",
            "bank_number"
        ]
        print(token)
        user = user_for_account(token.account)
        
        print(user)
        print('=============================================')
        
        if user == None:
            return {
                "type": "non_interactive_customer_info_needed",
                "fields": kyc_fields
            }
            
        print('=============================================')
        
        print('   request - >>>')
        print(request)
        print('   params - >>>')
        print(params)
        
        
        # user's KYC has been approved
        # transaction.amount_fee = calculate_fee(transaction)
        transaction.amount_out = round(
            transaction.amount_in - transaction.amount_fee,
            transaction.asset.significant_decimals
        )
        transaction.save()
        return {
            "how": (
                "Make a wire transfer to the following account. "
                "Accounting Number: 94922545 ; Routing Number: 628524560. "
                "Users MUST include the following memo: "
            ),
            "extra_info": {
                "accounting_number": "94922545",
                "routing_number": "628524560",
                "memo": f"memo",
            }
        }