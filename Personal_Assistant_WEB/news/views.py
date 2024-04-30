import environ
from django.shortcuts import render
from datetime import datetime, timedelta
from pathlib import Path
import requests
from django.core.cache import cache

from Personal_Assistant_WEB.settings import NEWSAPI_API_KEY  # noqa

BASE_DIR = Path(__file__).resolve().parent.parent.parent

CURRENT_DATE = datetime.now()
CURRENT_DATE_STR = CURRENT_DATE.strftime("%d.%m.%Y")

PRIVAT_URL = f"https://api.privatbank.ua/p24api/exchange_rates?date={CURRENT_DATE_STR}"

WAR_STATISTICS_URL = "https://russianwarship.rip/api/v2/statistics/latest/"

NEWS_DAYS = 2
NEWS_DATE = CURRENT_DATE - timedelta(days=NEWS_DAYS)
CURRENT_DATE_STR_NEWS = NEWS_DATE.strftime("%Y-%m-%d")
NEWS_TO_SHOW = 7

NEWSAPI_URL = f"https://newsapi.org/v2/top-headlines?country=ua&apiKey={NEWSAPI_API_KEY}"

# Cache keys
EXCHANGE_RATES_CACHE_KEY = 'exchange_rates'
WAR_STATS_CACHE_KEY = 'war_stats'
WAR_STATS_INCREASE_CACHE_KEY = 'war_stats_increase'
NEWS_ARTICLES_CACHE_KEY = 'news_articles'


def fetch_data(url):
    response = requests.get(url)
    return response.json()


def get_data_from_apis(urls):
    results = [fetch_data(url) for url in urls]
    return results


def news_view(request):
    # CHECKING IF DATA IS CACHED
    exchange_rates_cache = cache.get(EXCHANGE_RATES_CACHE_KEY)
    war_stats_cache = cache.get(WAR_STATS_CACHE_KEY)
    war_stats_increase_cache = cache.get(WAR_STATS_INCREASE_CACHE_KEY)
    news_articles_cache = cache.get(NEWS_ARTICLES_CACHE_KEY)

    if not (
            exchange_rates_cache and war_stats_cache and war_stats_increase_cache and news_articles_cache):

        urls = [PRIVAT_URL, WAR_STATISTICS_URL, NEWSAPI_URL]
        raw_data = get_data_from_apis(urls)

        exchange_rates = raw_data[0]["exchangeRate"]
        exchange_rate_data = []

        war_stats = raw_data[1]["data"]["stats"]
        war_stats_increase = raw_data[1]["data"]["increase"]

        news_articles = raw_data[2]["articles"][::-1]

        # Cache data for next request (15 minutes (900 seconds))
        cache.set(EXCHANGE_RATES_CACHE_KEY, exchange_rates, timeout=900)
        cache.set(WAR_STATS_CACHE_KEY, war_stats, timeout=900)
        cache.set(WAR_STATS_INCREASE_CACHE_KEY, war_stats_increase, timeout=900)
        cache.set(NEWS_ARTICLES_CACHE_KEY, news_articles, timeout=900)

        # IN CASE EXCHANGE RATES ARE NOT UPDATED
        for currency in ['USD', 'EUR', 'PLN']:
            try:
                sale_rate = next(rate["saleRate"] for rate in exchange_rates if rate["currency"] == currency)
                purchase_rate = next(rate["purchaseRate"] for rate in exchange_rates if rate["currency"] == currency)
            except StopIteration:
                sale_rate = "N/A"
                purchase_rate = "N/A"
            exchange_rate_data.append({'currency': currency, 'sale': sale_rate, 'purchase': purchase_rate})

        view_data = {
            'Date': raw_data[0]['date'],
            'Bank': 'PrivatBank',
            'Exchange_rate': exchange_rate_data,
            'War_day': raw_data[1]["data"]["day"],
            'Occupants_loses': {
                'personnel units': war_stats["personnel_units"],
                'tanks': war_stats["tanks"],
                'armoured fighting vehicles': war_stats["armoured_fighting_vehicles"],
                'artillery systems': war_stats["artillery_systems"],
                'mlrs': war_stats["mlrs"],
                'aa warfare systems': war_stats["aa_warfare_systems"],
                'planes': war_stats["planes"],
                'helicopters': war_stats["helicopters"],
                'vehicles fuel tanks': war_stats["vehicles_fuel_tanks"],
                'warships cutters': war_stats["warships_cutters"],
                'cruise missiles': war_stats["cruise_missiles"],
                'uav systems': war_stats["uav_systems"],
                'special military equip': war_stats["special_military_equip"],
                'submarines': war_stats["submarines"]
            },
            'Increase_by_day': {
                'personnel units': war_stats_increase["personnel_units"],
                'tanks': war_stats_increase["tanks"],
                'armoured fighting vehicles': war_stats_increase["armoured_fighting_vehicles"],
                'artillery systems': war_stats_increase["artillery_systems"],
                'mlrs': war_stats_increase["mlrs"],
                'aa warfare systems': war_stats_increase["aa_warfare_systems"],
                'planes': war_stats_increase["planes"],
                'helicopters': war_stats_increase["helicopters"],
                'vehicles fuel tanks': war_stats_increase["vehicles_fuel_tanks"],
                'warships cutters': war_stats_increase["warships_cutters"],
                'cruise missiles': war_stats_increase["cruise_missiles"],
                'uav systems': war_stats_increase["uav_systems"],
                'special military equip': war_stats_increase["special_military_equip"],
                'submarines': war_stats_increase["submarines"]
            },
            'News': [{
                "source": news_articles[i]["source"]["name"],
                "author": news_articles[i]["author"],
                "title": news_articles[i]["title"],
                "description": news_articles[i]["description"],
                "link_to_source": news_articles[i]["url"],
                "publishedAt": news_articles[i]["publishedAt"]
            } for i in range(NEWS_TO_SHOW)]
        }

    else:
        exchange_rate_data = []

        exchange_rates = exchange_rates_cache
        war_stats = war_stats_cache
        war_stats_increase = war_stats_increase_cache
        news_articles = news_articles_cache

        current_day = datetime.now()
        war_start_day = datetime(2022, 2, 23)
        war_days = (current_day - war_start_day).days

        # IN CASE EXCHANGE RATES ARE NOT UPDATED
        for currency in ['USD', 'EUR', 'PLN']:
            try:
                sale_rate = next(rate["saleRate"] for rate in exchange_rates if rate["currency"] == currency)
                purchase_rate = next(rate["purchaseRate"] for rate in exchange_rates if rate["currency"] == currency)
            except StopIteration:
                sale_rate = "N/A"
                purchase_rate = "N/A"
            exchange_rate_data.append({'currency': currency, 'sale': sale_rate, 'purchase': purchase_rate})

        view_data = {

            'Date': datetime.now().strftime("%d.%m.%Y"),
            'Bank': 'PrivatBank',
            'Exchange_rate': exchange_rate_data,
            'War_day': war_days,

            'Occupants_loses': {
                'personnel units': war_stats["personnel_units"],
                'tanks': war_stats["tanks"],
                'armoured fighting vehicles': war_stats["armoured_fighting_vehicles"],
                'artillery systems': war_stats["artillery_systems"],
                'mlrs': war_stats["mlrs"],
                'aa warfare systems': war_stats["aa_warfare_systems"],
                'planes': war_stats["planes"],
                'helicopters': war_stats["helicopters"],
                'vehicles fuel tanks': war_stats["vehicles_fuel_tanks"],
                'warships cutters': war_stats["warships_cutters"],
                'cruise missiles': war_stats["cruise_missiles"],
                'uav systems': war_stats["uav_systems"],
                'special military equip': war_stats["special_military_equip"],
                'submarines': war_stats["submarines"]
            },
            'Increase_by_day': {
                'personnel units': war_stats_increase["personnel_units"],
                'tanks': war_stats_increase["tanks"],
                'armoured fighting vehicles': war_stats_increase["armoured_fighting_vehicles"],
                'artillery systems': war_stats_increase["artillery_systems"],
                'mlrs': war_stats_increase["mlrs"],
                'aa warfare systems': war_stats_increase["aa_warfare_systems"],
                'planes': war_stats_increase["planes"],
                'helicopters': war_stats_increase["helicopters"],
                'vehicles fuel tanks': war_stats_increase["vehicles_fuel_tanks"],
                'warships cutters': war_stats_increase["warships_cutters"],
                'cruise missiles': war_stats_increase["cruise_missiles"],
                'uav systems': war_stats_increase["uav_systems"],
                'special military equip': war_stats_increase["special_military_equip"],
                'submarines': war_stats_increase["submarines"]
            },
            'News': [{
                "source": news_articles[i]["source"]["name"],
                "author": news_articles[i]["author"],
                "title": news_articles[i]["title"],
                "description": news_articles[i]["description"],
                "link_to_source": news_articles[i]["url"],
                "publishedAt": news_articles[i]["publishedAt"]
            } for i in range(NEWS_TO_SHOW)]
        }

    return render(request, 'news/index.html', context={'page_title': 'News and Statistics', 'data': view_data})
