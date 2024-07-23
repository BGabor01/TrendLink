from rest_framework import pagination
from rest_framework.response import Response


class CommentPagination(pagination.CursorPagination):
    page_size = 2
    ordering = "-created_at"

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


class PostCursorPagination(pagination.CursorPagination):
    page_size = 10
    ordering = "-created_at"
