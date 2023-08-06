from oauth2_provider.oauth2_validators import OAuth2Validator

class LongturnOAuth2Validator(OAuth2Validator):
    def get_additional_claims(self, request):
        return {
            "username": request.user.username,
        }
