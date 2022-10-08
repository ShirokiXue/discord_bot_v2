# [Task API](https://developers.google.com/tasks/reference/rest/)
# [Python Quickstart](https://developers.google.com/tasks/quickstart/python)
import json

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks']

class GoogleTaskManager:
    def __init__(self, jfile="json/bot_config.json") -> None:

        with open(jfile, 'r', encoding='utf8') as jfile:
            info = json.load(jfile)['google']['task']

        creds = Credentials.from_authorized_user_info(info, SCOPES)
        self.service = build('tasks', 'v1', credentials=creds)

    def get_task_lists(self)->dict:
        try:
            results = self.service.tasklists().list(maxResults=10).execute()
            return results.get('items', [])
        except HttpError as err:
            print(err)

    def get_tasks_from_list(self, list_id)->dict:
        try:
            results = self.service.tasks().list(tasklist=list_id).execute()
            return results.get('items', [])
        except HttpError as err:
            print(err)

    def get_task_with_id(self, tasklist, task)->dict:
        try:
            results = self.service.tasks().get(tasklist=tasklist, task=task).execute()
            return results
        except HttpError as err:
            print(err)

if __name__ == '__main__':
    task_manager = GoogleTaskManager()
    for task_list in task_manager.get_task_lists():
        print(f"{task_list['title']}: {task_list['id']}")

        tasks = task_manager.get_tasks_from_list(task_list['id'])
        is_parent_list = [task['parent'] if 'parent' in task else None for task in tasks]
        for task in tasks:
            if 'parent' in task: 
                parent = task_manager.get_task_with_id(task_list['id'], task['parent'])
                print(f"{parent['title']} - {task['title']}")
            elif task['id'] not in is_parent_list:
                print(f"{task['title']}")
            else:
                print(f"{task['title']} is a parent")