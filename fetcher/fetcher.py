import asyncio
import argparse
from asyncio import Queue
import aiohttp
import re
import json
from collections import Counter
import time

async def fetch_url(session, url, k):
    try:
        async with session.get(url, timeout=5) as resp:
            resp.raise_for_status()
            text = await resp.text()
            words = re.findall(r'\w+', text)
            local_counter = Counter(words)
            top = local_counter.most_common(k)
            json_string = json.dumps(dict(top))
            print(f"[{url}] => {json_string}")
            return text
        
    except aiohttp.ClientResponseError as e:
        print(f"Ошибка от {url}: {e}")
    except aiohttp.http_exceptions.LineTooLong as e:
        print(f"Пропущен (слишком длинный заголовок): {url}")
    except Exception as e:
        print(f"Иная ошибка от {url}: {e}")


async def fetch_data(worker_id, urls_que, session, k):
        while True:
            url = await urls_que.get()
            if url is None:
                urls_que.task_done()
                break
            try:
                print(f"[Worker {worker_id}] Начало обработки: {url}")
                await(fetch_url(session, url, k))
                print(f"[Worker {worker_id}] Обработан: {url}")
            finally:
                if url is not None:
                    urls_que.task_done()
async def main(c, k, url_file):
    t1 = time.time()
    async with aiohttp.ClientSession() as session:
        urls_que = asyncio.Queue()

        workers = [
            asyncio.create_task(
                fetch_data(worker_id, urls_que, session, k)
            )
            for worker_id in range(c)
        ]
    
        with open(url_file, "r", encoding='UTF-8') as file:
            for line in file:
                url = line.strip()
                if url:
                    await urls_que.put(url)

        for _ in range(c):
            await urls_que.put(None)

        await urls_que.join()
        await asyncio.gather(*workers)

        t2 = time.time()
        print(f"Время выполнения: {t2 - t1:.2f} сек")

def run_from_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", type=int, default=10, help="Количество воркеров")
    parser.add_argument("-k", type=int, default=4, help="Сколько слов выводить")
    parser.add_argument('url_file', help="Файл с URL-ами")
    args = parser.parse_args()
    asyncio.run(main(args.c, args.k, args.url_file))

if __name__ == "__main__":
    run_from_cli()

