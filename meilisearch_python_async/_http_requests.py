from __future__ import annotations

from typing import Any, Callable

from httpx import (
    AsyncClient,
    ConnectError,
    ConnectTimeout,
    HTTPError,
    RemoteProtocolError,
    Response,
)

from meilisearch_python_async.errors import MeiliSearchApiError, MeiliSearchCommunicationError


class _HttpRequests:
    def __init__(self, http_client: AsyncClient) -> None:
        self.http_client = http_client

    async def _send_request(
        self,
        http_method: Callable,
        path: str,
        body: Any | None = None,
    ) -> Response:
        try:
            response = None

            if not body:
                response = await http_method(path)
            else:
                response = await http_method(path, json=body)

            response.raise_for_status()
            return response

        except RemoteProtocolError as err:
            raise MeiliSearchCommunicationError(str(err)) from err
        except ConnectError as err:
            raise MeiliSearchCommunicationError(str(err)) from err
        except ConnectTimeout as err:
            raise MeiliSearchCommunicationError(str(err)) from err
        except HTTPError as err:
            if response:
                raise MeiliSearchApiError(str(err), response) from err

            raise

    async def get(self, path: str) -> Response:
        return await self._send_request(self.http_client.get, path)

    async def post(self, path: str, body: Any | None = None) -> Response:
        return await self._send_request(self.http_client.post, path, body)

    async def put(self, path: str, body: Any | None = None) -> Response:
        return await self._send_request(self.http_client.put, path, body)

    async def delete(self, path: str, body: dict | None = None) -> Response:
        return await self._send_request(self.http_client.delete, path, body)