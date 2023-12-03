def value_from_db(db_value):
    normal = 10 ** (db_value / 10)
    return normal

print(f"{value_from_db(-16):.4f}")
