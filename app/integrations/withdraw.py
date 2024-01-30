from decimal import Decimal
from typing import Optional, Dict, List
from django import forms
from django.http import JsonResponse
from rest_framework.request import Request
from polaris.models import Transaction, Asset
from polaris.templates import Template
from .forms import WithdrawForm, ConfirmationForm
from urllib.parse import (urlparse, parse_qs, urlencode, quote_plus)
from polaris.integrations import (
  WithdrawalIntegration, 
  TransactionForm 
)

class AnchorWithdraw(WithdrawalIntegration):
    def form_for_transaction(
        self,
        request: Request,
        transaction: Transaction,
        post_data: dict = None,
        amount: Decimal = None,
        *args,
        **kwargs
    ) -> Optional[forms.Form]:
        # if we haven't collected amount, collect it
        if not transaction.amount_in:
            if post_data:
                return WithdrawForm(transaction, post_data)
            else:
                return WithdrawForm(transaction, initial={"amount": amount})
        # we don't have anything more to collect
        else:
            return None

    def content_for_template(
        self,
        request: Request,
        template: Template,
        form: Optional[forms.Form] = None,
        transaction: Optional[Transaction] = None,
        *args,
        **kwargs,
    ) -> Optional[Dict]:
        if template == Template.WITHDRAW:
            if not form:  # we're done
                return None
            elif isinstance(form, WithdrawForm):
                return {
                    "title": ("Withdrawal Transaction Form"),
                    "guidance": (
                        "Please enter amount you would like to withdraw from wallet"
                    ),
                    "icon_label": ("NGNC Anchor Withdraw"),
                    # "icon_path": "image/NGNC.png",
                    # "show_fee_table": False,
                }
        elif  template == Template.MORE_INFO:
            # provides a label for the image displayed at the top of each page
            content = {
                "title": ("Asset Selection Form"),
                "icon_label": ("NGNC Anchor Withdraw"),
                # "icon_path": "image/NGNC.png"
            }
            return content
    
    def after_form_validation(
        self,
        request: Request,
        form: forms.Form,
        transaction: Transaction,
        *args,
        **kwargs,
    ):
        if isinstance(form, WithdrawForm ):
            # Polaris automatically assigns amount to Transaction.amount_in
           transaction.save()
    
    def interactive_url(
        self,
        request: Request,
        transaction: Transaction,
        asset: Asset,
        amount: Optional[Decimal],
        callback: Optional[str],
        *args: List,
        **kwargs: Dict,
    ) -> Optional[str]:
        if request.query_params.get("step"):
          raise NotImplementedError()

        # ownUrl = "http://localhost:3000/stellar_withdraw_1"
        ownUrl = "https://ngnc.online/stellar_withdraw_1"
        
         # Full interactive url /sep24/transactions/deposit/webapp
        url = request.build_absolute_uri()
        
        parsed_url = urlparse(url)

        query_result = parse_qs(parsed_url.query)

        token = (query_result['token'][0]) 

        ownUrl += "?" if parsed_url.query else "&"

        payload = {'type': 'withdraw', 'asset_code': asset.code, 'transaction_id':transaction.id, 'token': token, 'callback': callback, 'wallet': transaction.stellar_account}
        result = urlencode(payload, quote_via=quote_plus)
        # The anchor uses a standalone interactive flow
        return (ownUrl + result)

    def after_interactive_flow(
        self, 
        request: Request, 
        transaction: Transaction
    ):
        transaction.status = Transaction.STATUS.pending_user_transfer_start
        transaction.amount_in = Decimal(request.query_params.get("amount"))
        transaction.amount_fee = Decimal(request.query_params.get("amount_fee"))
        transaction.amount_out = transaction.amount_in - transaction.amount_fee
        transaction.memo_type = (request.query_params.get("memo_type"))
        transaction.memo = (request.query_params.get("hashed"))
        transaction.to_address = (request.query_params.get("account"))
        transaction.external_transaction_id = (request.query_params.get("externalId"))
        transaction.on_change_callback = (request.query_params.get("callback"))
        transaction.receiving_anchor_account = "GASBV6W7GGED66MXEVC7YZHTWWYMSVYEY35USF2HJZBLABLYIFQGXZY6"
        transaction.save()
