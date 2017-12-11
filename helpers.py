from urllib.parse import urlparse


class DomainHelpers:

    @staticmethod
    def get_domain_name(url):
        try:
            results = DomainHelpers.__get_sub_domain_name(url).split('.')
            return results[-2] + '.' + results[-1]
        except:
            return ''

    @staticmethod
    def __get_sub_domain_name(url):
        return urlparse(url).netloc
