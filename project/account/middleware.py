from django.shortcuts import redirect
from django.urls import reverse

from social_core.exceptions import AuthAlreadyAssociated
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
# social_django
class FacebookAuthAlreadyAssociatedMiddleware(SocialAuthExceptionMiddleware):
    """Redirect users to desired-url when AuthAlreadyAssociated exception occurs."""
    def process_exception(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            if request.backend.name == "facebook":
                message = "This facebook account is already in use."
                if message in str(exception):
                    # Add logic if required

                    # User is redirected to any url you want
                    # in this case to "app_name:url_name"
                    return redirect(reverse("home:home"))


# from django.shortcuts import redirect
# from django.urls import reverse
# from social_auth.middleware import SocialAuthExceptionMiddleware

# from social_core.exceptions import AuthAlreadyAssociated

# class FacebookAuthAlreadyAssociatedMiddleware(SocialAuthExceptionMiddleware):
#     """Redirect users to desired-url when AuthAlreadyAssociated exception occurs."""
#     def process_exception(self, request, exception):
#         if isinstance(exception, AuthAlreadyAssociated):
#             if request.backend.name == "facebook":
#                 message = "This facebook account is already in use."
#                 if message in str(exception):
#                     # Add logic if required

#                     # User is redirected to any url you want
#                     # in this case to "app_name:url_name"
#                     return redirect(reverse("home:home"))