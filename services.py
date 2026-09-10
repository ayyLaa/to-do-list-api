import storage
from schemas import TaskCreate, TaskUpdate
from typing import Optional



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


def get_tasks_filtered(done: Optional[bool] = None, search: Optional[str] = None):

    tasks = storage.get_all_items()


    if done is not None:
        tasks = [t for t in tasks if t['done'] == done]


    if search is not None:
        tasks = [t for t in tasks if search.lower() in t['title'].lower()]

    return tasks


def calculate_stats():
    tasks = storage.get_all_items()

    total = len(tasks)

    done_count = sum(1 for t in tasks if t['done'])
    open_count = total - done_count

    return {
        "total": total,
        "done": done_count,
        "open": open_count
    }