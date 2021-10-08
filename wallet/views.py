from .models import CustomerWallet, Transaction
from rest_framework.decorators import api_view
from rest_framework import status

from .utils import transform_response, validate_token
from .serializers import CreateWalletSerializer, TransactionSerializer
from rest_framework.response import Response


@api_view(['POST'])
def create_wallet(request):
    request_body = request.data
    serializer = CreateWalletSerializer(data=request_body)
    if serializer.is_valid():
        customer_wallet = CustomerWallet.objects.create(
            customer_xid=request_body.get('customer_xid')
        )
        response_data = {
            'token': customer_wallet.token
        }
        return Response(transform_response(response_data), status=status.HTTP_201_CREATED)
    else:
        response_data = {
            'error': serializer.errors
        }
        return Response(transform_response(response_data, status='fail'), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PATCH'])
def enable_disable_wallet(request):
    headers = request.headers
    is_valid, customer_wallet = validate_token(headers)
    if is_valid:
        #   POST
        if request.method == 'POST':
            if customer_wallet.enable_wallet():
                response_data = {
                    'wallet': {
                        'id': customer_wallet.id,
                        'owned_by': customer_wallet.customer_xid,
                        'status': 'enabled',
                        'enable_at': customer_wallet.enable_at,
                        'balance': customer_wallet.balance
                    }
                }
                return Response(transform_response(response_data), status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    'error': 'Already enabled'
                }
                return Response(transform_response(response_data, status='fail'), status=status.HTTP_400_BAD_REQUEST)
    #    GET
        elif request.method == 'GET':
            if customer_wallet.status:
                response_data = {
                    'wallet': {
                        'id': customer_wallet.id,
                        'owned_by': customer_wallet.customer_xid,
                        'status': 'enabled',
                        'enable_at': customer_wallet.enable_at,
                        'balance': customer_wallet.balance
                    }
                }
                return Response(transform_response(response_data), status=status.HTTP_200_OK)
            else:
                response_data = {
                    'error': 'Disabled'
                }
                return Response(transform_response(response_data, status='fail'), status=status.HTTP_400_BAD_REQUEST)
    #    PATCH
        elif request.method == 'PATCH':
            customer_wallet.disable_wallet()
            response_data = {
                'wallet': {
                    'id': customer_wallet.id,
                    'owned_by': customer_wallet.customer_xid,
                    'status': 'disabled',
                    'enable_at': customer_wallet.enable_at,
                    'balance': customer_wallet.balance
                }
            }
            return Response(transform_response(response_data), status=status.HTTP_200_OK)

    else:
        response_data = {
            'error': 'Invalid Token'
        }
        return Response(transform_response(response_data, status='fail'), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def deposit_wallet(request):
    headers = request.headers
    is_valid, customer_wallet = validate_token(headers)
    if is_valid:
        request_body = request.data
        serializer = TransactionSerializer(data=request_body)
        if serializer.is_valid():
            customer_wallet.deposit(
                headers['token'], serializer.data['amount'])
            transaction = Transaction.objects.create(
                customer_wallet=customer_wallet,
                transaction_type='D',
                amount=serializer.data['amount'],
                reference_id=serializer.data['reference_id']
            )

            response_data = {
                'id': transaction.id,
                'deposited_by': customer_wallet.customer_xid,
                'status': 'success',
                'deposited_at': transaction.transaction_date,
                'amount': transaction.amount,
                'referrence_id': transaction.reference_id
            }

            return Response(transform_response(response_data, status='success'), status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'error': serializer.errors
            }
            return Response(transform_response(response_data, status='fail'), status=status.HTTP_400_BAD_REQUEST)

    else:
        response_data = {
            'error': 'Invalid Token'
        }
        return Response(transform_response(response_data, status='fail'), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def withdraw_wallet(request):
    headers = request.headers
    is_valid, customer_wallet = validate_token(headers)
    if is_valid:
        request_body = request.data
        serializer = TransactionSerializer(data=request_body)
        if serializer.is_valid():
            if customer_wallet.withdraw(headers['token'], serializer.data['amount']):
                transaction = Transaction.objects.create(
                    customer_wallet=customer_wallet,
                    transaction_type='W',
                    amount=serializer.data['amount'],
                    reference_id=serializer.data['reference_id']
                )

                response_data = {
                    'id': transaction.id,
                    'withdraw_by': customer_wallet.customer_xid,
                    'status': 'success',
                    'withdraw_at': transaction.transaction_date,
                    'amount': transaction.amount,
                    'referrence_id': transaction.reference_id
                }

                return Response(transform_response(response_data, status='success'), status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    'error': 'Withdrawal amoun exceeded the current balance'
                }
                return Response(transform_response(response_data, status='fail'), status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data = {
                'error': serializer.errors
            }
            return Response(transform_response(response_data, status='fail'), status=status.HTTP_400_BAD_REQUEST)

    else:
        response_data = {
            'error': 'Invalid Token'
        }
        return Response(transform_response(response_data, status='fail'), status=status.HTTP_400_BAD_REQUEST)
