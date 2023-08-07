import asyncio
import httpx
import tqdm


async def download_files(url: str, filename: str):
    with open(filename, 'wb') as f:
        async with httpx.AsyncClient() as client:
            async with client.stream('GET', url) as r:
                
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))

                tqdm_params = {
                    'desc': url,
                    'total': total,
                    'miniters': 1,
                    'unit': 'it',
                    'unit_scale': True,
                    'unit_divisor': 1024,
                }

                with tqdm.tqdm(**tqdm_params) as pb:
                    async for chunk in r.aiter_bytes():
                        pb.update(len(chunk))
                        f.write(chunk)


async def main():

    loop = asyncio.get_running_loop()

    urls = [
        ('http://ipv4.download.thinkbroadband.com/50MB.zip', '50MB.zip'),
        ('http://ipv4.download.thinkbroadband.com/200MB.zip', '200MB.zip'),
        ('http://ipv4.download.thinkbroadband.com/20MB.zip', '20MB.zip'),
    ]

    tasks = [loop.create_task(download_files(url, filename)) for url, filename in urls]
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())
