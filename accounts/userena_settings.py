

ANONYMOUS_USER_ID = -1

AUTH_PROFILE_MODULE = 'accounts.Profile'

# Django Settings
LOGIN_URL = '/accounts/login/'

LOGOUT_URL = '/signout/'

LOGIN_REDIRECT_URL = '/accounts/loginredirect/'

# Userena Settings

USERENA_ACTIVATED = 'ALREADY_ACTIVATED'

USERENA_ACTIVATION_REQUIRED = False

USERENA_ACTIVATION_DAYS = 7

USERENA_ACTIVATION_NOTIFY = True

USERENA_ACTIVATION_NOTIFY_DAYS = 5

USERENA_ACTIVATION_RETRY = False

USERENA_DEFAULT_PRIVACY = 'open'

USERENA_DISABLE_PROFILE_LIST = False

USERENA_DISABLE_SIGNUP = False

USERENA_FORBIDDEN_USERNAMES = (
    'signup',
    'signout',
    'signin',
    'login',
    'activate',
    'me',
    'password',
)

USERENA_HIDE_EMAIL = False

USERENA_HTML_EMAIL = False

USERENA_LANGUAGE_FIELD = 'language'

USERENA_MUGSHOT_GRAVATAR = True

#USERENA_MUGSHOT_GRAVATAR_SECURE = USERENA_USE_HTTPS

USERENA_MUGSHOT_DEFAULT = 'mm'

USERENA_MUGSHOT_SIZE = 80

USERENA_MUGSHOT_CROP_TYPE = 'smart'

USERENA_MUGSHOT_PATH = 'mugshots/'

USERENA_PROFILE_DETAIL_TEMPLATE = 'userena/profile_detail.html'

USERENA_PROFILE_LIST_TEMPLATE = 'userena/profile_list.html'

USERENA_REDIRECT_ON_SIGNOUT = '/'

USERENA_REGISTER_PROFILE = True

USERENA_REGISTER_USER = True

USERENA_REMEMBER_ME_DAYS = (
    'a month',
    30,
)

USERENA_SIGNIN_AFTER_SIGNUP = True

USERENA_SIGNIN_REDIRECT_URL = '/loginredirect/'

USERENA_USE_HTTPS = False

USERENA_USE_MESSAGES = False

USERENA_USE_PLAIN_TEMPLATE = True

USERENA_WITHOUT_USERNAMES =  True
