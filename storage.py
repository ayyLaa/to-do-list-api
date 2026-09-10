db = {}

def save_item(id: int, title: str, done: bool):
    db[id] = {
        'id': id,
        'title': title,
        'done': done
    }

def get_item(id: int):
    if id in db:
        return db[id]
    else:
        return None

def get_all_items():
    return list(db.values())

def get_next_id():
    if not db:
        return 1
    return max(db.keys()) + 1



# Test data

save_item(1, "Buy milk", True)
save_item(2, "Do A1", False)