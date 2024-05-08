from news.views import news_view  # noqa


def main(request):
    return news_view(request)
