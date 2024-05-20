import logging
import asyncio
import aiohttp
from selenium.webdriver.common.by import By

async def check_link(session, url):
    try:
        async with session.head(url, allow_redirects=True) as response:
            if response.status >= 400:
                return url
    except aiohttp.ClientError:
        return url
    return None

async def check_links(session, links):
    tasks = [check_link(session, link) for link in links]
    return await asyncio.gather(*tasks)

async def find_broken_links(driver):
    links = [a.get_attribute('href') for a in driver.find_elements(By.TAG_NAME, 'a') if a.get_attribute('href')]
    
    broken_links = []
    async with aiohttp.ClientSession() as session:
        results = await check_links(session, links)
        broken_links = [result for result in results if result is not None]
    
    logging.info(f"Broken links: {broken_links}.")
    return broken_links
