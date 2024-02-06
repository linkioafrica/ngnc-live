from typing import Dict, List
from polaris.integrations import CustomerIntegration
from polaris.sep10.token import SEP10Token
from polaris.models import Transaction
from rest_framework.request import Request
from .users import user_for_account, fields_for_type, save_customer

class AnchorCustomer(CustomerIntegration):
    def get(
        self,
        token: SEP10Token,
        request: Request,
        params: Dict,
        *args: List,
        **kwargs: Dict
    ) -> Dict:
        
        print('-----------------------------------------------')
        print('customer', token)
        
        fields = fields_for_type(params.get("type"))

        return {
            "status": "NEEDS_INFO",
            "fields": fields
        }

        # user = user_for_account(
        #     token.muxed_account or token.account,
        #     token.memo or params.get("memo"),
        #     "id" if token.memo else params.get("memo_type")
        # )
        # fields = fields_for_type(params.get("type"))
        # if not user:
        #     return {
        #         "status": "NEEDS_INFO",
        #         "fields": fields
        #     }
        # missing_fields = dict([
        #     (f, v) for f, v in fields.items()
        #     if not getattr(user, f, False)
        # ])
        # provided_fields = dict([
        #     (f, v) for f, v in fields.items()
        #     if getattr(user, f, False)
        # ])
        # if missing_fields:
        #     return {
        #         "id": user.id,
        #         "status": "NEEDS_INFO",
        #         "fields": missing_fields,
        #         "provided_fields": provided_fields
        #     }
        # if user.rejected:
        #     return {
        #         "id": user.id,
        #         "status": "REJECTED",
        #         "provided_fields": provided_fields
        #     }
        # if user.kyc_approved:
        #     return {
        #         "id": user.id,
        #         "status": "APPROVED",
        #         "provided_fields": provided_fields
        #     }
        # return {
        #     "id": user.id,
        #     "status": "PENDING",
        #     "provided_fields": provided_fields
        # }

    def put(
        self,
        token: SEP10Token,
        request: Request,
        params: Dict,
        *args: List,
        **kwargs: Dict
    ) -> str:
        
        print('-------------------- PUT ------------------')
        print(token.account)
        print('request = ', request)
        print('params = ', params)
        print('args = ', args)
        print('kwargs = ', kwargs)
        
        # params:
        # {'account': 'GBSN6X2PKNSVIUN5QB6XKL64T3J375ZPDLMZSS62T7ZGLNJRPFIAJ266', 'asset': <Asset: NGNC - issuer(GCUNL4X72TO6D62UB6ABMJBFNWIJFTAJM6N3IGUNW6AFITTYQ4JWKPX6)>, 'memo_type': None, 'memo': None, 'lang': 'en', 'type': 'undefined', 'claimable_balance_supported': False, 'on_change_callback': None, 'country_code': None, 'amount': Decimal('12345.00'), 'quote': None, 'source_asset': None, 'asset_code': 'NGNC'}
                
        customer = save_customer(token.account, params)
        if customer == None:
            return ""
        return str(customer.id)