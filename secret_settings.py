"""
Contains all the secrets for the website. Production uses a different file, that is not pushed to github.
"""

import json
import os

secrets = {
    "SECRET_KEY": "j@7*rtssewjfhix2f^7&1iypigm=o4ju1qtdd!)ad$s1*hlkj2",
    "DEBUG": True,
    "ALLOWED_HOSTS": [],
    "LOGGING": {"FOLDER": "logs"},
    "DATABASES": {
        "DEFAULT": {
            "NAME": "cosmos_website_test",
            "USER": "cosmos_website_tester",
            "PASSWORD": "2020123",
            "HOST": "",
            "PORT": "",
            "OPTIONS": {"options": "-c search_path=public"},
        },
        "LEGACY": {
            "NAME": "cosmos_website_test_legacy",
            "USER": "cosmos_website_tester_legacy",
            "PASSWORD": "2020123",
            "HOST": "",
            "PORT": "",
            "OPTIONS": {"options": "-c search_path=public"},
        },
    },
    "EMAIL": {
        "HOST": "smtp.sendgrid.net",
        "PORT": 587,
        "USERNAME": "apikey",
        "PASSWORD": "fakekey",
        "USE_TLS": True,
    },
    # Gmail SMTP Relay
    # https://support.google.com/a/answer/2956491?hl=en
    "EMAIL_GSUITE": {
        "HOST": "smtp-relay.gmail.com",
        "PORT": 587,
        "USERNAME": "noreply@cosmostue.nl",
        "PASSWORD": "fakepassword",
        "USE_TLS": True,
    },
    "PRETIX_DOMAIN": "http://localhost:8345",
    # TODO store tokens per team
    "PRETIX_AUTHORIZATION_HEADER": {
        "Authorization": "Token qe7op3k271qtdi1pspbdpxlhcm7oyve4fgkxdrkcucrjmiwdey8bdebcokz4ar8y"
    },
}

if os.path.exists("/etc/secrets.json"):
    with open("/etc/secrets.json", "r") as f:
        secrets = json.load(f)
elif os.path.exists("tests/secrets.json"):
    with open("tests/secrets.json", "r") as f:
        secrets = json.load(f)
