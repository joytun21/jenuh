def get_value(key):
    with open("kyt/var.txt") as f:
        for line in f:
            if line.startswith(key + "="):
                return line.strip().split("=", 1)[1]
    return None

BOT_TOKEN = get_value("BOT_TOKEN")
ADMIN = int(get_value("ADMIN")) if get_value("ADMIN") else None
