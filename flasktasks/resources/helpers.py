from typing import Mapping

from flasktasks.config import settings


def paginate[T](elements: list[T], params: Mapping[str, str]) -> list[T]:
    """Given a list of elements, return page `from_idx` for page size `page_size`.

    The typehints use Python3.12's new typevar syntax.
    In practice, this means this function is dependent on some type T that is unknown,
    but `elements` is a list of this type,
    and the return type is also a list of this type as well.
    """
    page_from = int(params.get("page", 1))
    page_size = int(params.get("size", settings.page_size))

    page = elements[(page_from - 1) * page_size : page_from * page_size]
    return page
