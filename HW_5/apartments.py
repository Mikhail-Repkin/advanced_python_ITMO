import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
from aiomisc import new_event_loop, PeriodicCallback

BASE_URL = "https://realty.ya.ru/moskva/snyat/kvartira/"
FILE_PATH = "artifacts/apartments.csv"


async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()


async def scrape_yandex(session, url):
    html = await fetch_html(session, url)
    soup = BeautifulSoup(html, "html.parser")

    listings = []

    # Извлечение информации о квартирах
    items = soup.find_all("li", class_="OffersSerpItem")
    for item in items:
        listing = {}
        listing["title"] = item.find(
            "span", class_="OffersSerpItem__title"
        ).text.strip()
        listing["building"] = item.find(
            "div", class_="OffersSerpItem__building"
        ).text.strip()
        listing["price"] = item.find(
            "div", class_="OffersSerpItem__price"
        ).text.strip()
        listing["address"] = item.find(
            "div", class_="OffersSerpItem__address"
        ).text.strip()
        listing["metro"] = item.find(class_="MetroStation__title").text.strip()
        listing["description"] = item.find(
            class_="OffersSerpItem__description"
        ).text.strip()
        listing["link"] = (f"https://realty.ya.ru/"
                           f"{item.find('a', class_='OffersSerpItem__link').get('href')}")
        listings.append(listing)

    return listings


async def save_listings_to_txt(listings):
    df = pd.DataFrame(listings)
    mode = 'a' if FILE_PATH else 'w'
    df.to_csv(FILE_PATH,
              mode=mode,
              index=False,
              sep='|',
              )


async def main():
    async with aiohttp.ClientSession() as session:
        try:
            listings = await scrape_yandex(session, BASE_URL)
            await save_listings_to_txt(listings)
            print(f"Scraped {len(listings)} apartments. Data saved to file.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    loop = new_event_loop()
    periodic = PeriodicCallback(main)
    try:
        periodic.start(300, delay=0)
        loop.run_forever()
    except KeyboardInterrupt:
        print('Manually closed application')
    finally:
        periodic.stop()
        loop.run_until_complete(asyncio.sleep(0))
        loop.close()
        print('loop is closed')
