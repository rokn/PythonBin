import requests
import validators
import settings

_user_key = None

def login_user(username, password):
    global _user_key
    data = {
            'api_dev_key': settings.PASTEBIN_API_KEY,
            'api_user_name': username,
            'api_user_password': password
        }
    resp = requests.post(settings.PASTEBIN_USER_LOGIN_URL, data)
    result = {
            'data': resp.text,
            'success': True
        }
    if result['data'].lower().startswith('bad'):
        result['success'] = False
    else:
        _user_key = result['data']

    return result

def paste_create(content, title, syntax, expiry):
    data = {
            'api_dev_key': settings.PASTEBIN_API_KEY,
            'api_option': settings.PASTEBIN_API_PASTE_OPTION,
            'api_paste_code': content,
        }
    if title:
        data['api_paste_name'] = title
    if syntax:
        data['api_paste_format'] = title
    if expiry:
        data['api_paste_expire_date'] = expiry

    if _user_key: 
        data['api_user_key'] = _user_key
    resp = requests.post(settings.PASTEBIN_CREATE_URL, data)
    result = {
            'data': resp.text,
            'success': True
        }
    if not validators.url(result['data']):
        result['success'] = False

    return result
