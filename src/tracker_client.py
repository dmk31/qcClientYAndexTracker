import os
from dotenv import load_dotenv
from yandex_tracker_client import TrackerClient

# Загружаем переменные окружения из .env файла
load_dotenv()

class YandexTrackerClient:
    """
    Класс для работы с Yandex Tracker API.
    Позволяет получать списки задач по различным фильтрам.
    """

    def __init__(self):
        """
        Инициализация клиента Yandex Tracker.
        Токен и org_id берутся из переменных окружения.
        """
        self.token = os.getenv('YANDEX_TRACKER_TOKEN')
        self.org_id = os.getenv('YANDEX_TRACKER_ORG_ID')

        if not self.token or not self.org_id:
            raise ValueError("Необходимо установить YANDEX_TRACKER_TOKEN и YANDEX_TRACKER_ORG_ID в .env файле")

        self.client = TrackerClient(token=self.token, org_id=self.org_id)

    def get_issues_by_queue(self, queue, limit=50):
        """
        Получить список задач по очереди.

        :param queue: Название очереди (например, 'MYQUEUE')
        :param limit: Максимальное количество задач для возврата
        :return: Список объектов задач
        """
        try:
            issues = self.client.issues.find(
                filter={'queue': queue},
                per_page=limit
            )
            return list(issues)
        except Exception as e:
            print(f"Ошибка при получении задач по очереди {queue}: {e}")
            return []

    def get_issues_by_filter(self, filter_dict, limit=50):
        """
        Получить список задач по произвольному фильтру.

        :param filter_dict: Словарь с фильтрами (например, {'queue': 'MYQUEUE', 'assignee': 'me()'})
        :param limit: Максимальное количество задач для возврата
        :return: Список объектов задач
        """
        try:
            issues = self.client.issues.find(
                filter=filter_dict,
                per_page=limit
            )
            return list(issues)
        except Exception as e:
            print(f"Ошибка при получении задач по фильтру {filter_dict}: {e}")
            return []

    def get_issues_by_assignee(self, assignee, limit=50):
        """
        Получить список задач по исполнителю.

        :param assignee: Логин исполнителя (например, 'me()' для текущего пользователя)
        :param limit: Максимальное количество задач для возврата
        :return: Список объектов задач
        """
        return self.get_issues_by_filter({'assignee': assignee}, limit)

    def get_issues_by_author(self, author, limit=50):
        """
        Получить список задач по автору.

        :param author: Логин автора задачи
        :param limit: Максимальное количество задач для возврата
        :return: Список объектов задач
        """
        return self.get_issues_by_filter({'author': author}, limit)