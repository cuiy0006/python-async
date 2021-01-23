#!/usr/bin/env python3

import re
from typing import IO
import urllib.error
import urllib.parse
import aiofiles
import aiohttp
from aiohttp import ClientSession
import asyncio

HREF_RE = re.compile(r'href="(.*?)"')

async def fetch_html(url: str, session: ClientSession) -> str:
    resp = await session.request(method='GET', url=url)
    print(f'Got response {resp.status} for URL: {url}')
    html = ''
    if resp.status == 200:
        html = await resp.text()
    return html

async def parse(url: str, session: ClientSession) -> set:
    found = set()
    html = await fetch_html(url=url, session=session)

    for link in HREF_RE.findall(html):
        try:
            abslink = urllib.parse.urljoin(url, link)
        except (urllib.error.URLError, ValueError):
            print(f'Error parsing link: {link}')
        else:
            found.add(abslink)
    print(f'Found {len(found)} links for {url}')
    return found

async def write_one(file: IO, url: str, session: ClientSession) -> None:
    '''Write the found HREFs from `url` to `file`.'''
    found = await parse(url=url, session=session)
    if not found:
        return
    async with aiofiles.open(file, 'a') as f:
        for abslink in found:
            await f.write(f'{url}\t{abslink}\n')
        print(f'Wrote results for source URL: {url}')

async def bulk_crawl_and_write(file: IO, urls: set) -> None:
    '''Crawl & write concurrently to `file` for multiple `urls`.'''
    async with ClientSession() as session:
        coros = []
        for url in urls:
            coros.append(
                write_one(file=file, url=url, session=session)
            )
        await asyncio.gather(*coros)

if __name__ == '__main__':
    import pathlib
    import sys

    assert sys.version_info >= (3, 7), 'Script requires Python 3.7+.'
    here = pathlib.Path(__file__).parent

    with open(here.joinpath('urls.txt'), 'r') as infile:
        urls = set(map(str.strip, infile.readlines()))

    outpath = here.joinpath('foundurls.txt')
    with open(outpath, 'w') as outfile:
        outfile.write('source_url\tparsed_url\n')

    asyncio.run(bulk_crawl_and_write(file=outpath, urls=urls))