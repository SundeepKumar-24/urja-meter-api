
from unittest.mock import patch

from app import create_app


def setup_client():
    app = create_app({
        "TESTING": True,
        "PORTAL_METERS_URL": "https://example.test/meters",
        "PORTAL_TRANSFORMERS_URL": "https://example.test/transformers",
        "PORTAL_ENERGY_URL": "https://example.test/meters/{meter_id}/energy",
        "PORTAL_GEO_URL": "https://example.test/meters/{meter_id}/geo",
        "PORTAL_COOKIE": "",
        "PORTAL_BEARER_TOKEN": "",
        "REQUEST_TIMEOUT_SECONDS": 2,
    })
    return app.test_client()


def test_health():
    client = setup_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_invalid_page_returns_400():
    client = setup_client()
    response = client.get("/api/v1/meters?page=abc")

    assert response.status_code == 400
    assert response.json["error"] == "invalid_page"


@patch("app.routes.get_json")
def test_meters_returns_portal_data(mock_get_json):
    mock_get_json.return_value = {
        "data": [{"meterId": "J100000"}],
        "page": 1,
        "pageSize": 20,
        "total": 1,
    }

    client = setup_client()
    response = client.get("/api/v1/meters?page=1")

    assert response.status_code == 200
    assert response.json["data"][0]["meterId"] == "J100000"


@patch("app.routes.get_json")
def test_unknown_meter_preserves_404(mock_get_json):
    from app.portal_client import PortalRequestError

    mock_get_json.side_effect = PortalRequestError(
        "Portal returned HTTP 404.",
        status_code=404,
    )

    client = setup_client()
    response = client.get("/api/v1/meters/UNKNOWN123/geo")

    assert response.status_code == 404
    assert response.json["error"] == "portal_request_failed"

def test_invalid_transformer_page_returns_400():
    client = setup_client()

    response = client.get("/api/v1/transformers?page=abc")

    assert response.status_code == 400
    assert response.json["error"] == "invalid_page"
