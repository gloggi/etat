from django.http import HttpResponseRedirect
from django.conf import settings

class LoginRequiredMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            if request.path_info != settings.LOGIN_URL:
                return HttpResponseRedirect(settings.LOGIN_URL)