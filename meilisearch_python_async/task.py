from __future__ import annotations

from asyncio import sleep
from datetime import datetime
from typing import TYPE_CHECKING
from urllib.parse import urlencode

from httpx import AsyncClient

from meilisearch_python_async._http_requests import HttpRequests
from meilisearch_python_async.errors import MeiliSearchTimeoutError
from meilisearch_python_async.models.task import TaskInfo, TaskStatus

if TYPE_CHECKING:
    from meilisearch_python_async.client import Client  # pragma: no cover


async def cancel_tasks(
    client: AsyncClient | Client,
    *,
    uids: list[str] | None = None,
    index_uids: list[str] | None = None,
    statuses: list[str] | None = None,
    types: list[str] | None = None,
    before_enqueued_at: datetime | None = None,
    after_enqueueda_at: datetime | None = None,
    before_started_at: datetime | None = None,
    after_finished_at: datetime | None = None,
) -> TaskInfo:
    """Cancel a list of enqueued or processing tasks.

    Defaults to cancelling all tasks.

    Args:

        client: An httpx AsyncClient or meilisearch_python_async Client instance.
        uids: A list of task UIDs to cancel.
        index_uids: A list of index UIDs for which to cancel tasks.
        statuses: A list of statuses to cancel.
        types: A list of types to cancel.
        before_enqueued_at: Cancel tasks that were enqueued before the specified date time.
        after_enqueueda_at: Cancel tasks that were enqueued after the specified date time.
        before_started_at: Cancel tasks that were started before the specified date time.
        after_finished_at: Cancel tasks that were finished after the specified date time.

    Returns:

        The details of the task

    Raises:

        MeilisearchCommunicationError: If there was an error communicating with the server.
        MeilisearchApiError: If the MeiliSearch API returned an error.
        MeiliSearchTimeoutError: If the connection times out.

    Examples:

        >>> from meilisearch_python_async import Client
        >>> from meilisearch_python_async.task import cancel_tasks
        >>>
        >>> async with Client("http://localhost.com", "masterKey") as client:
        >>>     await cancel_tasks(client, uids=[1, 2])
    """
    parameters = {}
    if uids:
        parameters["uids"] = ",".join([str(x) for x in uids])
    if index_uids:
        parameters["indexUids"] = ",".join([str(x) for x in index_uids])
    if statuses:
        parameters["statuses"] = ",".join(statuses)
    if types:
        parameters["types"] = ",".join(types)
    if before_enqueued_at:
        parameters["beforeEnqueuedAt"] = str(before_enqueued_at)
    if after_enqueueda_at:
        parameters["afterEnqueuedAt"] = str(after_enqueueda_at)
    if before_started_at:
        parameters["beforeStartedAt"] = str(before_started_at)
    if after_finished_at:
        parameters["afterFinishedAt"] = str(after_finished_at)

    if not parameters:
        # Cancel all tasks if no parmaeters provided
        parameters["statuses"] = "enqueued,processing"

    url = f"tasks/cancel?{urlencode(parameters)}"
    client_ = _get_client(client)
    response = await client_.post(url)

    return TaskInfo(**response.json())


async def delete_tasks(
    client: AsyncClient | Client,
    *,
    uids: list[str] | None = None,
    index_uids: list[str] | None = None,
    statuses: list[str] | None = None,
    types: list[str] | None = None,
    before_enqueued_at: datetime | None = None,
    after_enqueueda_at: datetime | None = None,
    before_started_at: datetime | None = None,
    after_finished_at: datetime | None = None,
) -> TaskInfo:
    """Delete a list of tasks.

    Defaults to deleting all tasks.

    Args:

        client: An httpx AsyncClient or meilisearch_python_async Client instance.
        uids: A list of task UIDs to cancel.
        index_uids: A list of index UIDs for which to cancel tasks.
        statuses: A list of statuses to cancel.
        types: A list of types to cancel.
        before_enqueued_at: Cancel tasks that were enqueued before the specified date time.
        after_enqueueda_at: Cancel tasks that were enqueued after the specified date time.
        before_started_at: Cancel tasks that were started before the specified date time.
        after_finished_at: Cancel tasks that were finished after the specified date time.

    Returns:

        The details of the task

    Raises:

        MeilisearchCommunicationError: If there was an error communicating with the server.
        MeilisearchApiError: If the MeiliSearch API returned an error.
        MeiliSearchTimeoutError: If the connection times out.

    Examples:

        >>> from meilisearch_python_async import Client
        >>> from meilisearch_python_async.task import delete_tasks
        >>>
        >>> async with Client("http://localhost.com", "masterKey") as client:
        >>>     await delete_tasks(client, uids=[1, 2])
    """
    parameters = {}
    if uids:
        parameters["uids"] = ",".join([str(x) for x in uids])
    if index_uids:
        parameters["indexUids"] = ",".join([str(x) for x in index_uids])
    if statuses:
        parameters["statuses"] = ",".join(statuses)
    if types:
        parameters["types"] = ",".join(types)
    if before_enqueued_at:
        parameters["beforeEnqueuedAt"] = str(before_enqueued_at)
    if after_enqueueda_at:
        parameters["afterEnqueuedAt"] = str(after_enqueueda_at)
    if before_started_at:
        parameters["beforeStartedAt"] = str(before_started_at)
    if after_finished_at:
        parameters["afterFinishedAt"] = str(after_finished_at)

    if not parameters:
        # delete all tasks if no parmaeters provided
        parameters["statuses"] = "canceled,enqueued,failed,processing,succeeded"

    url = f"tasks?{urlencode(parameters)}"
    client_ = _get_client(client)
    response = await client_.delete(url)

    return TaskInfo(**response.json())


async def get_tasks(
    client: AsyncClient | Client,
    *,
    index_ids: list[str] | None = None,
    types: str | list[str] | None = None,
) -> list[TaskStatus]:
    """Get multiple tasks.

    Args:

        client: An httpx AsyncClient or meilisearch_python_async Client instance.
        index_ids: A list of index UIDs for which to get the tasks. If provided this will get the
            tasks only for the specified indexes, if not all tasks will be returned. Default = None
        types: Specify specific task types to retrieve. Default = None

    Returns:

        A list of all tasks.

    Raises:

        MeilisearchCommunicationError: If there was an error communicating with the server.
        MeilisearchApiError: If the MeiliSearch API returned an error.
        MeiliSearchTimeoutError: If the connection times out.

    Examples:

        >>> from meilisearch_python_async import Client
        >>> from meilisearch_python_async.task import get_tasks
        >>>
        >>> async with Client("http://localhost.com", "masterKey") as client:
        >>>     await get_tasks(client)
    """
    url = f"tasks?indexUids={','.join(index_ids)}" if index_ids else "tasks"
    if types:
        formatted_types = ",".join(types) if isinstance(types, list) else types
        url = f"{url}&types={formatted_types}" if "?" in url else f"{url}?types={formatted_types}"
    client_ = _get_client(client)
    response = await client_.get(url)

    return [TaskStatus(**x) for x in response.json()["results"]]


async def get_task(client: AsyncClient | Client, task_id: int) -> TaskStatus:
    """Get a single task from it's task id.

    Args:

        client: An httpx AsyncClient or meilisearch_python_async Client instance.
        task_id: Identifier of the task to retrieve.

    Returns:

        A list of all tasks.

    Raises:

        MeilisearchCommunicationError: If there was an error communicating with the server.
        MeilisearchApiError: If the MeiliSearch API returned an error.
        MeiliSearchTimeoutError: If the connection times out.

    Examples:

        >>> from meilisearch_python_async import Client
        >>> from meilisearch_python_async.task import get_task
        >>>
        >>> async with Client("http://localhost.com", "masterKey") as client:
        >>>     await get_task(client, 1244)
    """
    client_ = _get_client(client)
    response = await client_.get(f"tasks/{task_id}")

    return TaskStatus(**response.json())


async def wait_for_task(
    client: AsyncClient | Client,
    task_id: int,
    *,
    timeout_in_ms: int = 5000,
    interval_in_ms: int = 50,
) -> TaskStatus:
    """Wait until MeiliSearch processes a task, and get its status.

    Args:

        client: An httpx AsyncClient or meilisearch_python_async Client instance.
        task_id: Identifier of the task to retrieve.
        timeout_in_ms: Amount of time in milliseconds to wait before raising a
            MeiliSearchTimeoutError. Defaults to 5000.
        interval_in_ms: Time interval in miliseconds to sleep between requests. Defaults to 50.

    Returns:

        Details of the processed update status.

    Raises:

        MeilisearchCommunicationError: If there was an error communicating with the server.
        MeilisearchApiError: If the MeiliSearch API returned an error.
        MeiliSearchTimeoutError: If the connection times out.

    Examples:

        >>> from meilisearch_python_async import Client
        >>> from meilisearch_python_async.task import wait_for_task
        >>> >>> documents = [
        >>>     {"id": 1, "title": "Movie 1", "genre": "comedy"},
        >>>     {"id": 2, "title": "Movie 2", "genre": "drama"},
        >>> ]
        >>> async with Client("http://localhost.com", "masterKey") as client:
        >>>     index = client.index("movies")
        >>>     response = await index.add_documents(documents)
        >>>     await wait_for_pending_task(client, response.update_id)
    """
    client_ = _get_client(client)
    url = f"tasks/{task_id}"
    http_requests = HttpRequests(client_)
    start_time = datetime.now()
    elapsed_time = 0.0
    while elapsed_time < timeout_in_ms:
        response = await http_requests.get(url)
        status = TaskStatus(**response.json())
        if status.status in ("succeeded", "failed"):
            return status
        await sleep(interval_in_ms / 1000)
        time_delta = datetime.now() - start_time
        elapsed_time = time_delta.seconds * 1000 + time_delta.microseconds / 1000
    raise MeiliSearchTimeoutError(
        f"timeout of {timeout_in_ms}ms has exceeded on process {task_id} when waiting for pending update to resolve."
    )


def _get_client(client: AsyncClient | Client) -> AsyncClient:
    if isinstance(client, AsyncClient):
        return client

    return client.http_client
