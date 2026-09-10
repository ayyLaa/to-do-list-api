import storage
from schemas import TaskCreate, TaskUpdate



def create_new_task(task_data: TaskCreate):
    new_id = storage.get_next_id()

    new_task = storage.save_item(id=new_id, title=task_data.title, done=False)
    return new_task

def update_task(id: int, update_data: TaskUpdate):
    return storage.update_item(
        id = id,
        title = update_data.title,
        done = update_data.done,
    )

def delete_task(id: int):
    storage.delete_item(id)