import re
# import phonenumbers

# from django.conf import settings

EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def check_if_username_email_mobile(username):

    if '@' in username and '.' in username:
        return 'email'

    elif username.replace('+', '').isdigit():
        return 'mobile'

    return None

def validate_email(username):

    validation = re.match(EMAIL_PATTERN, username)
    if validation:
        return True, "Success"
    else:
        return False, "Invalid Email in Username"


def validate_mobile(username):

    # try:
    #     number = phonenumbers.parse(
    #         username, settings.PHONENUMBER_DEFAULT_REGION)
    # except Exception as e:
    #     print(str(e))
    #     return False, "Not Country specific phone number"
    # if not phonenumbers.is_valid_number(number):
    #     return False, "Invalid phone number"

    return True, "Success"