import click
from .tracker_client import YandexTrackerClient
from tabulate import tabulate
from colorama import init, Fore, Style

# Инициализация colorama для Windows
init(autoreset=True)

def format_issues_table(issues):
    """
    Форматирует список задач в табличный вид для вывода в консоль.

    :param issues: Список объектов задач
    :return: Отформатированная строка таблицы
    """
    if not issues:
        return f"{Fore.YELLOW}Задачи не найдены.{Style.RESET_ALL}"

    headers = ['Ключ', 'Название', 'Статус', 'Исполнитель', 'Автор', 'Создано']
    table_data = []

    for issue in issues:
        table_data.append([
            issue.key,
            issue.summary[:50] + '...' if len(issue.summary) > 50 else issue.summary,
            getattr(issue, 'status', {}).get('name', 'Неизвестно'),
            getattr(issue, 'assignee', {}).get('display', 'Не назначен'),
            getattr(issue, 'author', {}).get('display', 'Неизвестен'),
            getattr(issue, 'createdAt', 'Неизвестно')[:10]  # Только дата
        ])

    return tabulate(table_data, headers=headers, tablefmt='grid')

@click.group()
def cli():
    """CLI инструмент для работы с Yandex Tracker."""
    pass

@cli.command()
@click.argument('queue')
@click.option('--limit', default=50, help='Максимальное количество задач для вывода')
def queue(queue, limit):
    """Получить задачи по очереди."""
    try:
        client = YandexTrackerClient()
        issues = client.get_issues_by_queue(queue, limit)
        click.echo(f"{Fore.GREEN}Найдено задач: {len(issues)}{Style.RESET_ALL}")
        click.echo(format_issues_table(issues))
    except Exception as e:
        click.echo(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")

@cli.command()
@click.argument('assignee')
@click.option('--limit', default=50, help='Максимальное количество задач для вывода')
def assignee(assignee, limit):
    """Получить задачи по исполнителю."""
    try:
        client = YandexTrackerClient()
        issues = client.get_issues_by_assignee(assignee, limit)
        click.echo(f"{Fore.GREEN}Найдено задач: {len(issues)}{Style.RESET_ALL}")
        click.echo(format_issues_table(issues))
    except Exception as e:
        click.echo(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")

@cli.command()
@click.argument('author')
@click.option('--limit', default=50, help='Максимальное количество задач для вывода')
def author(author, limit):
    """Получить задачи по автору."""
    try:
        client = YandexTrackerClient()
        issues = client.get_issues_by_author(author, limit)
        click.echo(f"{Fore.GREEN}Найдено задач: {len(issues)}{Style.RESET_ALL}")
        click.echo(format_issues_table(issues))
    except Exception as e:
        click.echo(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")

@cli.command()
@click.option('--queue', help='Очередь')
@click.option('--assignee', help='Исполнитель')
@click.option('--author', help='Автор')
@click.option('--status', help='Статус')
@click.option('--limit', default=50, help='Максимальное количество задач для вывода')
def filter(queue, assignee, author, status, limit):
    """Получить задачи по произвольному фильтру."""
    filter_dict = {}
    if queue:
        filter_dict['queue'] = queue
    if assignee:
        filter_dict['assignee'] = assignee
    if author:
        filter_dict['author'] = author
    if status:
        filter_dict['status'] = status

    if not filter_dict:
        click.echo(f"{Fore.YELLOW}Не указан ни один фильтр. Используйте --help для справки.{Style.RESET_ALL}")
        return

    try:
        client = YandexTrackerClient()
        issues = client.get_issues_by_filter(filter_dict, limit)
        click.echo(f"{Fore.GREEN}Найдено задач: {len(issues)}{Style.RESET_ALL}")
        click.echo(format_issues_table(issues))
    except Exception as e:
        click.echo(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")

if __name__ == '__main__':
    cli()