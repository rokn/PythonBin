import requests
import validators
import settings

def paste_create(content):
    data = {
            'api_dev_key': settings.PASTEBIN_API_KEY,
            'api_option': settings.PASTEBIN_API_PASTE_OPTION,
            'api_paste_code': content
        }
    resp = requests.post(settings.PASTE_CREATE_URL, data)
    result = {
            'url': resp.text,
            'success': True
        }
    if not validators.url(result['url']):
        result['success'] = False

    return result
