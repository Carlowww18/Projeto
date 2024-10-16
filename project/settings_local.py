# settings_local.py

# Importa todas as configurações padrões do settings.py
from .settings import *

# Sobrescreve apenas a configuração do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Você também pode modificar outras configurações locais, se necessário.
