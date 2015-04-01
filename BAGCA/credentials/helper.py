from .models import Credentials

def populate_with_default_info(request):
    EMAIL_HOST_USER = 'bagca.training@gmail.com'
    EMAIL_HOST_PASSWORD = 'adminpassw'
    DROPBOX_API_KEY = '4JihgFtwf1AAAAAAAAAABVhYGDbBX9DoeDmPUEnu5FtnJALyAIQvb0JoV-TSZCwm'

    dropbox_api_key = Credentials(credential='Dropbox', value=DROPBOX_API_KEY)
    dropbox_api_key.save()