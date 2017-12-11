from worker import Worker
from db_queue import *
from spider import Spider
from helpers import DomainHelpers
import project_settings


def execute():
    project_name = ''
    home_page = ''
    thread_count = 8

    # project_name must be provided, the program will use this variable as the database tables' prefix
    while project_name == '':
        project_name = input('Please give a name to the project:')

    print('Project name is', project_name)

    while home_page == '':
        home_page = input('Please input the home page to start:')

    regx_home_page = re.compile(r'^http[s]?://.+$')
    if not regx_home_page.match(home_page):
        print('{} is not a valid home page'.format(home_page))
        exit()  # if home_page url is not valid, the program will stop

    print('Home page is', home_page)

    new_thread_count = input('Change worker number or use {} with just leaving it blank:'.format(thread_count))

    if new_thread_count:
        try:
            thread_count = int(new_thread_count)
            print('New work number is ', thread_count)
        except ValueError:
            print('Your input is not a valid number, worker number will be:', thread_count)

    (lambda x: globals()[x])(project_settings.DB_CLASS_NAME)(home_page, project_name + '_pages')
    Spider(home_page, DomainHelpers.get_domain_name(home_page), project_settings.HTML_RESOLVER_NAME)

    worker = Worker(thread_count, project_name)
    worker.create_threads()
    worker.crawl()


execute()
