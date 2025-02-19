from typing import Iterable, Dict

from fastapi import APIRouter, HTTPException


def include_routers(root_router: APIRouter, routers: Iterable[APIRouter]) -> APIRouter:
    for router in routers:
        root_router.include_router(router)
    return root_router


def build_exception_responses(*exceptions: HTTPException) -> Dict:
    result = {}
    for exc in exceptions:
        if exc.status_code not in result:
            result[exc.status_code] = [exc.detail]
        else:
            result[exc.status_code].append(exc.detail)

    return {
        status_code: {
            'content': {
                'application/json': {
                    'examples': {
                        detail: {
                            'value': {'details': detail}
                        }
                        for detail in details
                    }
                }
            },
        }
        for status_code, details in result.items()
    }