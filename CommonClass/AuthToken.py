import requests, os

def getCurrentSessionToken(token_url, client_id, client_secret, logger, payload=None):
    try:
        url = token_url
        headers = {
            'client_id': client_id,
            'client_secret': client_secret
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('Auth token generated successfully with the client id of: ' + client_id)
        os.environ['jwt-token'] = response.headers.get('jwt-token')

    except requests.ConnectionError as error:
        logger.error("Connection error during authentication, exception is:" + str(error))