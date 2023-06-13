from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
from polaris.utils import getLogger
import jwt
import json
import os
import environ

logger = getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.dirname(BASE_DIR)


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def callback(request):
    """
    The URL for this endpoint is can be used by clients as the on_change_callback URL
    to test Polaris' on_change_callback requests.
    """
    print(request)
    logger.info(
        f"on_change_callback request received: {json.dumps(request.data, indent=2)}"
    )
    return Response({"status": "ok"}, status=200)

env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file):  
    env.read_env(env_file)

@csrf_exempt
def onCallback(request):
    print(request.method)
    if request.method == 'POST':
        # logger.info(
        #     f"on_change_callback request received: {json.dumps(request.POST, indent=2)}"
        # )
        # response = {'status': 'OK', 'message': 'valid request method'}
        # return JsonResponse(response, status=200)

        # Retrieve the JSON payload from the POST request
        data = request.POST.get('jwt')

        # Decode and verify the JWT token
        try:
            decoded_token = jwt.decode(data, os.environ['SECRET_KEY'], algorithms=['HS256'])
            # Extract the necessary information from the decoded token
            account_id = decoded_token['account_id']
            token = decoded_token['token']
            print(account_id, token)

            # Validate the token and perform necessary actions
            if validate_token(token):
                # Process the account data and take appropriate actions
                process_account_data(account_id)

                # Return a success response
                response = {'status': 'success'}
                return JsonResponse(response, status=200)
            else:
                # Return an error response
                response = {'status': 'error', 'message': 'Invalid token'}
                return JsonResponse(response, status=400)
        except jwt.ExpiredSignatureError:
            # Handle expired token
            response = {'status': 'error', 'message': 'Expired token'}
            return JsonResponse(response, status=400)
    else:
        # Handle invalid request method
        response = {'status': 'error', 'message': 'Invalid request method'}
        return JsonResponse(response, status=405)

def validate_token(token):
    try:
        # Add your token validation logic here
        # For example, verify the token's signature using a secret key
        decoded_token = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=['HS256'])
        # Additional validation checks if required
        # ...
        return True
    except jwt.InvalidTokenError:
        return False

def process_account_data(account_id):
    # Add your logic to process the account data
    # Perform the necessary actions based on the account information
    print("Processing account data for account ID:", account_id)
