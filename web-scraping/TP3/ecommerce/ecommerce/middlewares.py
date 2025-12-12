# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class UserAgentMiddleware:

    def __init__(self):
        # Liste d'exemples de User-Agent. D'autres valeurs peuvent être ajoutées.
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"

    def process_request(self, request, spider):
        """
        Modifie l'en-tête HTTP 'User-Agent' de la requête.

        Cette méthode est appelée pour chaque Request avant l'envoi
        par le Downloader. Le middleware choisit un User-Agent au hasard
        dans la liste et le place dans les en-têtes.
        """
        request.headers['User-Agent'] = self.user_agent