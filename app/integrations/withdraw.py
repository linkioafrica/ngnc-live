from decimal import Decimal
from typing import Optional, Dict, List
from django import forms
from rest_framework.request import Request
from polaris.models import Transaction, Asset
from polaris.templates import Template
from .forms import WithdrawForm, ConfirmationForm
from urllib.parse import (urlparse, urlencode, quote_plus)
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
                    "title": ("Witdrawal Transaction Form"),
                    "guidance": (
                        "Please enter amount you would like to withdraw from wallet"
                    ),
                    "icon_label": ("NGNX Anchor Withdraw"),
                    # "icon_path": "image/NGNC.png",
                    "show_fee_table": False,
                }
        elif  template == Template.MORE_INFO:
            # provides a label for the image displayed at the top of each page
            content = {
                "title": ("Asset Selection Form"),
                "icon_label": ("NGNX Anchor Withdraw"),
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

        ownUrl = "https://ngnc.online/stellar/withdraw"
        url = request.build_absolute_uri()
        parsed_url = urlparse(url)
        ownUrl += "?" if parsed_url.query else "&"

        payload = {'asset_code': asset.code, 'transaction_id':transaction.id, 'type': 'withdraw', token: {token}}
        result = urlencode(payload, quote_via=quote_plus)
    
        # The anchor uses a standalone interactive flow
        return (ownUrl + result)

    def after_interactive_flow(
        self, 
        request: Request, 
        transaction: Transaction
    ):
        transaction.amount_out = Decimal(request.query_params.get("amount_out"))
        transaction.status = Transaction.STATUS.pending_user_transfer_start
        transaction.save()