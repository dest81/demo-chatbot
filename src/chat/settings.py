import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = '=fyn9+99bjlnadv$0%gowwl5nvg-%!*$2%uwg)v5@gh)lkpuwg'

DEBUG = True

ALLOWED_HOSTS = ['10.10.10.10']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chatterbot.ext.django_chatterbot',
    'channels',
    'chat_engine.apps.DefaultConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# bot = ChatBot(
#     'Default Response Example Bot',
#     storage_adapter='chatterbot.storage.SQLStorageAdapter',
#     logic_adapters=[
#         {
#             'import_path': 'chatterbot.logic.BestMatch'
#         },
#         {
#             'import_path': 'chatterbot.logic.LowConfidenceAdapter',
#             'threshold': 0.90,
#             'default_response': 'I am sorry, but I do not understand.'
#         }
#     ],
#     trainer='chatterbot.trainers.ListTrainer'
# )

CHATTERBOT = {
    'name': 'RIPY',
    'logic_adapters': [
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_random_response"
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.90,
            'default_response': 'I am sorry, but I do not understand.'
        }
    ],
    'trainer': 'chatterbot.trainers.ListTrainer',
    'django_app_name': 'django_chatterbot'
}

# CHATTERBOT = {
#     'name': 'RIPE Bot',
#     'trainer': 'chatterbot.trainers.ChatterBotCorpusTrainer',
#     'training_data': [
#         'chatterbot.corpus.english.ai',
#         'chatterbot.corpus.english.botprofile',
#         'chatterbot.corpus.english.computers',
#         'chatterbot.corpus.english.conversations',
#         'chatterbot.corpus.english.emotion',
#         'chatterbot.corpus.english.food',
#         'chatterbot.corpus.english.gossip',
#         'chatterbot.corpus.english.greetings',
#         'chatterbot.corpus.english.history',
#         'chatterbot.corpus.english.humor',
#         'chatterbot.corpus.english.literature',
#         'chatterbot.corpus.english.money',
#         'chatterbot.corpus.english.movies',
#         'chatterbot.corpus.english.politics',
#         'chatterbot.corpus.english.psychology',
#         'chatterbot.corpus.english.science',
#         'chatterbot.corpus.english.sports',
#         'chatterbot.corpus.english.trivia',
#     ],
#     'django_app_name': 'django_chatterbot'
# }

CHATTERBOT_CORPUS = {
    'name': 'RIPE Bot',
    'trainer': 'chatterbot.trainers.UbuntuCorpusTrainer',
    'django_app_name': 'django_chatterbot'
}

ROOT_URLCONF = 'chat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'chat', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chat.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'chatbot',
#         'USER': 'chatbot',
#         'PASSWORD': 'chatbot',     # noqa
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

LANGUAGE_CODE = 'en-us'
#LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'chat', 'static'),
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "chat.routing.routing",
    },
}
