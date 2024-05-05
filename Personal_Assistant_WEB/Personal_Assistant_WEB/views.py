from news.views import news_view  # noqa

from Personal_Assistant_WEB.settings import env  # noqa


def main(request):
    return news_view(request)
