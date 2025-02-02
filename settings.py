TORTOISE = {
    "connections": {
        "default": "sqlite://db.sqlite3"
    },
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                "ending.models"
            ],
            "default_connection": "default"
        }
    }
}
