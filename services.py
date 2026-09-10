import storage
from schemas import TaskCreate


def create_new_task(task_data: TaskCreate):
    new_id = storage.get_next_id()

    new_task = storage.save_item(id=new_id, title=task_data.title, done=False)
    return new_task