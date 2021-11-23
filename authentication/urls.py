from django.conf.urls import url
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from authentication.views import RegistrationView, LoginView, LogoutView

"""
    This is authentication URLS, Register, Login, Refresh and Verify and point for user and user token
    Methods: [POST]
    Endpoint: given below (stating with url(....))
    Example:
    {
        "username": "test@test.com",
        "password": "password"
    }
    
    Example: [POST] /api-token-auth/  data={"username": "test@test.com", "password": "password"}
"""
urlpatterns = [
    path('register/', RegistrationView.as_view()),
    # path('api-token-auth/', LoginView.as_view()), # for example purpose
    path('logout/', LogoutView.as_view()),
    url(r'^api-token-auth/', obtain_jwt_token),  # obtain jwt token
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]
