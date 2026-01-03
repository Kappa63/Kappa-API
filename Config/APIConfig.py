NOT_USER_RATELIMIT = "20/minute"
GENERAL_RATELIMIT = "50/minute"
PRIVATE_RATELIMIT = "100/minute"
ADMIN_RATELIMIT = "1000/minute"

CAREGIVER_RATELIMIT = "500/minute"

def SWAGGER_TEMPLATE(app_name: str):
    return {
        "swagger": "2.0",
        "info": {
            "title": app_name,
            "description": "The Kappa API",
            "version": "v2.0",
            "contact": {"email": "karim@qiblawi.dev"},
        },
        "basePath": "/api",
        "schemes": ["http"],
        "externalDocs": {
            "description": "GitHub Repository",
            "url": "https://github.com/Kappa63/Kappa-Api",
        },
    }

def SWAGGER_CONFIG(app_name: str):
    return {
        "headers": [],
        "specs": [
            {
                "endpoint": "APIDocs",
                "route": "/APIDocs",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True
            }
        ],
        "static_url_path": "/flasgger_static",
        "specs_route": "/",
        "title": app_name,
    }
