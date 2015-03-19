# Social Auth
LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/loginredirect/'
LOGIN_ERROR_URL    = '/error/'
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UUID_LENGTH = 16

SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'
SOCIAL_AUTH_ENABLED_BACKENDS = ('google', 'facebook', 'twitter')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SOCIAL_AUTH_PIPELINE_RESUME_ENTRY = 'accounts.pipeline.createProfile'



SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    #'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'accounts.pipeline.getProfileDetails',
    'accounts.pipeline.createProfile',
)
