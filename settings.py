from django.conf import settings


if hasattr(settings, 'PRODCAL_LOCALE_SUPPORTING'):
    LOCALE_SUPPORTING = settings.PRODCAL_LOCALE_SUPPORTING
else:
    LOCALE_SUPPORTING = (
        ("UA", "Україна"),
        ("PL", "Polska"),
        ("RU", "Россия"),
        ("KZ", "Kazakhstan"),
        ("BY", "Belarus"),
        ("GE", "Georgia"),
        ("EE", "Estonia"),
        ("DE", "Germany"),
        ("CN", "China"),
    )
if hasattr(settings, 'PRODCAL_DEFAULT_LOCALE'):
    DEFAULT_LOCALE = settings.PRODCAL_DEFAULT_LOCALE
else:
    DEFAULT_LOCALE = LOCALE_SUPPORTING[0][0]
if hasattr(settings, 'PRODCAL_DEFAULT_TIME_PER_DAY'):
    DEFAULT_TIME_PER_DAY = settings.PRODCAL_DEFAULT_TIME_PER_DAY
else:
    DEFAULT_TIME_PER_DAY = 8