from urllib.request import urlopen
from db_queue import *
from html_resolver import *
from helpers import DomainHelpers
import project_settings
import ssl


class Spider:
    DB = None
    BASE_URL = ''
    DOMAIN_NAME = ''
    HTML_RESOLVER = ''

    def __init__(self, base_url, domain_name, html_resolver):
        Spider.DB = (lambda x: globals()[x])(project_settings.DB_CLASS_NAME)
        Spider.BASE_URL = base_url
        Spider.DOMAIN_NAME = domain_name
        Spider.HTML_RESOLVER = html_resolver
        Spider.crawl_page('First spider', Spider.BASE_URL)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if Spider.DB.is_page_in_queue(page_url):
            print(thread_name + ' now crawling ' + page_url)
            urls = Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.DB.save_pending_queue(urls)
            Spider.DB.set_page_crawled(page_url)

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            # to make self-signed ssl works, pass variable 'context' to function 'urlopen'
            context = ssl._create_unverified_context()
            response = urlopen(page_url, context=context)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = (lambda x: globals()[x])(Spider.HTML_RESOLVER)(Spider.BASE_URL, page_url)
            # finder = HtmlResolver(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(urls):
        links = set()
        for url in urls:
            if Spider.DOMAIN_NAME != DomainHelpers.get_domain_name(url):
                continue
            links.add(url)
        return links
