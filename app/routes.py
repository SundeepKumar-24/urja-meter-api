
from flask import Blueprint, jsonify, request

from .portal_client import (
    get_json,
    PortalNotConfigured,
    PortalRequestError,
)

api = Blueprint("api", __name__)


@api.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "urja-meter-api",
    }), 200


def forward(config_key, params=None, path_values=None):
    try:
        data = get_json(
            config_key,
            params=params,
            path_values=path_values,
        )
        return jsonify(data), 200

    except PortalNotConfigured as exc:
        return jsonify({
            "error": "portal_not_configured",
            "message": str(exc),
        }), 503

    except PortalRequestError as exc:
        return jsonify({
            "error": "portal_request_failed",
            "message": str(exc),
        }), exc.status_code



@api.get("/api/v1/meters")
def meters():
    query = request.args.get("q", "")
    page_value = request.args.get("page", "1")

    try:
        page = int(page_value)
    except (TypeError, ValueError):
        return jsonify({
            "error": "invalid_page",
            "message": "The page parameter must be a positive integer."
        }), 400

    if page < 1:
        return jsonify({
            "error": "invalid_page",
            "message": "The page parameter must be a positive integer."
        }), 400

    params = {
        "q": query,
        "page": page,
    }
    return forward("PORTAL_METERS_URL", params=params)



@api.get("/api/v1/transformers")
def transformers():
    page_value = request.args.get("page", "1")

    try:
        page = int(page_value)
    except (TypeError, ValueError):
        return jsonify({
            "error": "invalid_page",
            "message": "The page parameter must be a positive integer.",
        }), 400

    if page < 1:
        return jsonify({
            "error": "invalid_page",
            "message": "The page parameter must be a positive integer.",
        }), 400

    return forward(
        "PORTAL_TRANSFORMERS_URL",
        params={"page": page},
    )


@api.get("/api/v1/meters/<meter_id>/energy")
def meter_energy(meter_id):
    return forward(
        "PORTAL_ENERGY_URL",
        path_values={"meter_id": meter_id},
    )


@api.get("/api/v1/meters/<meter_id>/geo")
def meter_geo(meter_id):
    return forward(
        "PORTAL_GEO_URL",
        path_values={"meter_id": meter_id},
    )
