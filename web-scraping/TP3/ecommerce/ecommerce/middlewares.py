# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html


class UserAgentMiddleware:

    def __init__(self):
        # User-agent
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"

def process_request(self, request, spider):
    """
    Modifies the HTTP 'User-Agent' header of the request.

    This method is called for each Request before it is sent
    by the Downloader.
    """
    request.headers['User-Agent'] = self.user_agent
