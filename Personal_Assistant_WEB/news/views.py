from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent.parent.parent

CURRENT_DATE = datetime.now()
CURRENT_DATE_STR = CURRENT_DATE.strftime("%d.%m.%Y")
PRIVAT_URL = f"https://api.privatbank.ua/p24api/exchange_rates?date={CURRENT_DATE_STR}"
WAR_STATISTICS_URL = "https://russianwarship.rip/api/v2/statistics/latest"
NEWS_DAYS = 2
NEWS_DATE = CURRENT_DATE - timedelta(days=NEWS_DAYS)
CURRENT_DATE_STR_NEWS = NEWS_DATE.strftime("%Y-%m-%d")
NEWS_TO_SHOW = 7
NEWSAPI_API_KEY = 'e8c7836e9cba4e558c25ef61be1b5f84'
NEWSAPI_URL = (f"https://newsapi.org/v2/everything?q=Apple&from={NEWS_DATE}&"
               f"sortBy=popularity&apiKey={NEWSAPI_API_KEY}")


def fetch_data(url):
    response = requests.get(url)
    return response.json()


def get_data_from_apis(urls):
    results = [fetch_data(url) for url in urls]
    return results


def news_view(request):
    urls = [PRIVAT_URL, WAR_STATISTICS_URL, NEWSAPI_URL]
    raw_data = get_data_from_apis(urls)
    war_stats = raw_data[1]["data"]["stats"]
    war_stats_increase = raw_data[1]["data"]["increase"]
    news_articles = raw_data[2]["articles"][::-1]
    view_data = {'Date': raw_data[0]['date'],
                 'Bank': 'PrivatBank',
                 'Exchange_rate': [{'currency': 'USD',
                                    'sale': next(rate["saleRate"] for rate in raw_data[0]["exchangeRate"] if
                                                 rate["currency"] == 'USD'),
                                    'purchase': next(rate["purchaseRate"] for rate in raw_data[0]["exchangeRate"] if
                                                     rate["currency"] == 'USD')},
                                   {'currency': 'EUR',
                                    'sale': next(rate["saleRate"] for rate in raw_data[0]["exchangeRate"] if
                                                 rate["currency"] == 'EUR'),
                                    'purchase': next(rate["purchaseRate"] for rate in raw_data[0]["exchangeRate"] if
                                                     rate["currency"] == 'EUR')},
                                   {'currency': 'PLN',
                                    'sale': next(rate["saleRate"] for rate in raw_data[0]["exchangeRate"] if
                                                 rate["currency"] == 'PLN'),
                                    'purchase': next(rate["purchaseRate"] for rate in raw_data[0]["exchangeRate"] if
                                                     rate["currency"] == 'PLN')}],
                 'War_day': raw_data[1]["data"]["day"],
                 'Occupants_loses': {'personnel units': war_stats["personnel_units"],
                                     'tanks': war_stats["tanks"],
                                     'armoured fighting vehicles': war_stats["armoured_fighting_vehicles"],
                                     'artillery systems': war_stats["artillery_systems"],
                                     'mlrs': war_stats["mlrs"],
                                     'aa warfare systems': war_stats["aa_warfare_systems"],
                                     'planes': war_stats["planes"],
                                     'helicopters': war_stats["helicopters"],
                                     'vehicles fuel tanks"': war_stats["vehicles_fuel_tanks"],
                                     'warships cutters': war_stats["warships_cutters"],
                                     'cruise missiles': war_stats["cruise_missiles"],
                                     'uav systems': war_stats["uav_systems"],
                                     'special military equip': war_stats["special_military_equip"],
                                     'submarines': war_stats["submarines"]},
                 'Increase_by_day': {'personnel units': war_stats_increase["personnel_units"],
                                     'tanks': war_stats_increase["tanks"],
                                     'armoured fighting vehicles': war_stats_increase[
                                         "armoured_fighting_vehicles"],
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
                                     'submarines': war_stats_increase["submarines"]},
                 'News': [{"source": news_articles[i]["source"]["name"],
                           "author": news_articles[i]["author"],
                           "title": news_articles[i]["title"],
                           "description": news_articles[i]["description"],
                           "link_to_source": news_articles[i]["url"],
                           "publishedAt": news_articles[i]["publishedAt"]} for i in range(NEWS_TO_SHOW)]
                 }

    return render(request, 'news/index.html',
                  context={'page_title': 'News and Statistics', 'data': view_data})
