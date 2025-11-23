def is_null_empty_space(val):
    if val is None or val.strip() == "":
        return True
    return False