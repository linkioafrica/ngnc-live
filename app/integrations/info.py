from rest_framework.request import Request
from polaris.models import Asset
from .. import settings


def info_integration(request: Request, asset: Asset, lang: str, *args, **kwargs):
  if asset.code == "NGNC":
    return {
      "deposit": 
      {
        "enabled": true,
        "min_amount": 0.1,
        "max_amount": 1000,
        "authentication_required": true,
      },
      "withdraw": 
      {
        "enabled": true,
        "authentication_required": true,
        "min_amount": 0.1,
        "max_amount": 1000
      },
      "transactions": 
      {
      "enabled": true, 
      },
      "transaction": 
      {
        "enabled": true,
      },
    },