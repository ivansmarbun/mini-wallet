from .models import CustomerWallet

def transform_response(data, status='success'):
    return {
        'status': status,
        'data': data
    }

def validate_token(headers):
    if headers.get('token'):
        customer_wallet = CustomerWallet.objects.filter(token=headers.get('token')).first()
        if customer_wallet:
            return (True, customer_wallet)
        return (False, None)
    else:
        return (False, None)