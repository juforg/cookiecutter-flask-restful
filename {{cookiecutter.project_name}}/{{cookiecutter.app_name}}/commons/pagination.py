"""Simple helper to paginate query
"""
from flask import url_for, request
from sqlalchemy import text

DEFAULT_PAGE_SIZE = 50
DEFAULT_PAGE_NUMBER = 1


def paginate(query, schema):
    page = int(request.args.get('page', DEFAULT_PAGE_NUMBER))
    per_page = int(request.args.get('pageSize', DEFAULT_PAGE_SIZE))
    sort = request.args.get("sort", None)
    if sort:
        query = query.order_by(text(sort))
    page_obj = query.paginate(page=page, per_page=per_page)
    next = url_for(
        request.endpoint,
        page=page_obj.next_num if page_obj.has_next else page_obj.page,
        pageSize=per_page,
        **request.view_args
    )
    prev = url_for(
        request.endpoint,
        page=page_obj.prev_num if page_obj.has_prev else page_obj.page,
        pageSize=per_page,
        **request.view_args
    )

    return {
        'total': page_obj.total,
        'pages': page_obj.pages,
        'next': next,
        'prev': prev,
        'items': schema.dump(page_obj.items)
    }
