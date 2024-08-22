from models import db, Task
from typing import List, Dict, Union, Optional


class TaskService:

    @staticmethod
    def get_all_tasks() -> List[Dict[str, Union[int, str]]]:
        tasks = Task.query.all()
        return [task.to_dict() for task in tasks]

    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Dict[str, Union[int, str]]]:
        task = Task.query.get(task_id)
        if task:
            return task.to_dict()
        return None

    @staticmethod
    def add_task(task_data: Dict[str, str]) -> Dict[str, Union[int, str]]:
        task = Task()
        task.task = task_data['task']
        db.session.add(task)
        db.session.commit()
        return task.to_dict()

    @staticmethod
    def delete_task(task_id: int) -> bool:
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return True
        return False
