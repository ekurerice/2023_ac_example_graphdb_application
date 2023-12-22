import pytest


class TestRouter:
    # get リクエスト

    data_for_test_get = [(200, "/v1/graphs", {"label": "individual", "name": "K"})]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("expected, end_point, params", data_for_test_get)
    @pytest.mark.limit_memory("24 MB")
    async def test_get(self, client, gremlin_service, expected, end_point, params):
        response = await client.get(end_point, json=params)
        assert expected == response.status_code

    # post vertex
    data_for_post_vertices = [
        (201, "/v1/graph/vertices", {"label": "individual", "name": "Z"})
    ]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("expected, endpoint, params", data_for_post_vertices)
    async def test_post_vertices(
        self, client, gremlin_service, expected, endpoint, params
    ):
        response = await client.post(endpoint, json=params)
        assert expected == response.status_code

    # post edge
    data_for_post_edges = [
        (
            201,
            "/v1/graph/edges",
            {
                "label": "label",
                "v1": {"label": "individual", "name": "A"},
                "v2": {"label": "individual", "name": "K"},
                "data": {"type": "additional"},
            },
        )
    ]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("expected, endpoint, params", data_for_post_edges)
    async def test_post_edges(
        self, client, gremlin_service, expected, endpoint, params
    ):
        response = await client.post(endpoint, json=params)
        assert expected == response.status_code
