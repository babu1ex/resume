import asyncio
import sys
from unittest.mock import AsyncMock, patch

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from  import fetch_url, fetch_data, main, run_from_cli


@pytest.mark.asyncio
async def test_fetch_url_success():
    with aioresponses() as m:
        m.get("http://example.com", status=200, body="cat dog cat lion")
        async with ClientSession() as session:
            result = await fetch_url(session, "http://example.com", k=2)
            assert "cat" in result


@pytest.mark.asyncio
async def test_fetch_url_client_response_error():
    with aioresponses() as m:
        m.get("http://bad-url.com", status=404)
        async with ClientSession() as session:
            result = await fetch_url(session, "http://bad-url.com", k=2)
            assert result is None


@pytest.mark.asyncio
async def test_fetch_url_timeout_error():
    with aioresponses() as m:
        m.get("http://timeout.com", exception=asyncio.TimeoutError)
        async with ClientSession() as session:
            result = await fetch_url(session, "http://timeout.com", k=2)
            assert result is None


@pytest.mark.asyncio
async def test_fetch_url_generic_error():
    with aioresponses() as m:
        m.get("http://oops.com", exception=Exception("Unexpected"))
        async with ClientSession() as session:
            result = await fetch_url(session, "http://oops.com", k=2)
            assert result is None


@pytest.mark.asyncio
async def test_fetch_data_processes_url():
    queue = asyncio.Queue()
    session = AsyncMock()
    session.get.return_value.__aenter__.return_value.text.return_value = "hello world"
    await queue.put("http://test.com")
    await queue.put(None)

    with patch("fetcher.fetch_url", new=AsyncMock(return_value="response")) as mock_fetch:
        await fetch_data(worker_id=1, urls_que=queue, session=session, k=2)
        mock_fetch.assert_called_once_with(session, "http://test.com", 2)


@pytest.mark.asyncio
async def test_main_runs_all_workers(tmp_path):
    url_file = tmp_path / "urls.txt"
    url_file.write_text("http://a.com\nhttp://b.com\n")

    with patch("fetcher.fetch_url", new=AsyncMock(return_value="data")) as mock_fetch:
        try:
            await asyncio.wait_for(
                main(c=2, k=2, url_file=str(url_file)),
                timeout=3
            )
        except asyncio.TimeoutError:
            pytest.fail("main завис — возможно, воркеры не завершились")

        assert mock_fetch.call_count == 2


def test_run_from_cli_runs_main():
    test_args = ["script_name", "-c", "3", "-k", "2", "urls.txt"]

    with patch.object(sys, "argv", test_args), \
         patch("fetcher.main", new=AsyncMock()) as mock_main:
        run_from_cli()
        mock_main.assert_awaited_once_with(3, 2, "urls.txt")
