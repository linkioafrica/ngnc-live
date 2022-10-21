from decimal import Decimal
from typing import Optional, Dict, List
from django import forms
from rest_framework.request import Request
from polaris.models import Transaction, Asset
from polaris.templates import Template
from .forms import DepositForm
from urllib.parse import (urlparse, urlencode, quote_plus)
from polaris.integrations import (
    DepositIntegration,
    TransactionForm
)

class AnchorDeposit(DepositIntegration):
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
                return DepositForm(transaction, post_data)
            else:
                return DepositForm(transaction, initial={"amount": amount})
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
        if template == Template.DEPOSIT:
            if not form:  # we're done
                return None
            elif isinstance(form, DepositForm):
                return {
                    "title": ("Deposit Transaction Form"),
                    "guidance": (
                        "Provide all info enquired below"
                    ),
                    "icon_label": ("NGNX Anchor Deposit"),
                    # "icon_path": "image/NGNC.png"
                }
        elif  template == Template.MORE_INFO:
            # provides a label for the image displayed at the top of each page
            content = {
                "title": ("Asset Selection Form"),
                "guidance": (
                    "If business or recipient doesn’t have, generate one and send"
                ),
                "icon_label": ("Stellar Development Foundation"),
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
        if isinstance(form, DepositForm ):
            # Polaris automatically assigns amount to Transaction.amount_in
           transaction.save()
    
    def after_deposit(self, transaction: Transaction, *args, **kwargs):
        transaction.channel_seed = None
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

        ownUrl = "https://ngnc.online/stellar/deposit"
        url = request.build_absolute_uri()
        parsed_url = urlparse(url)
        ownUrl += "?" if parsed_url.query else "&"

        payload = {'asset_code': asset.code, 'transaction_id':transaction.id, 'type': 'deposit', 'callback': callback}
        result = urlencode(payload, quote_via=quote_plus)
        # The anchor uses a standalone interactive flow
        return (ownUrl + result)

    def after_interactive_flow(
        self, 
        request: Request, 
        transaction: Transaction
    ):
        transaction.amount_in = Decimal(request.query_params.get("amount_in"))
        transaction.status = Transaction.STATUS.pending_user_transfer_start
        transaction.save()