
import requests
from flask import current_app


class PortalNotConfigured(Exception):
    pass


class PortalRequestError(Exception):
    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.status_code = status_code


def get_json(config_key, params=None, path_values=None):
    """Send a GET request to the configured portal endpoint."""

    url = current_app.config.get(config_key)

    if not url:
        raise PortalNotConfigured(
            f"{config_key} is empty. Check your .env file."
        )

    # Replace URL placeholders such as {meter_id}.
    if path_values:
        try:
            url = url.format(**path_values)
        except KeyError as exc:
            raise PortalNotConfigured(
                f"Missing URL value: {exc}"
            ) from exc

    headers = {"Accept": "application/json"}

    token = current_app.config.get("PORTAL_BEARER_TOKEN")
    cookie = current_app.config.get("PORTAL_COOKIE")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    if cookie:
        headers["Cookie"] = cookie

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=current_app.config["REQUEST_TIMEOUT_SECONDS"],
        )

        response.raise_for_status()

        try:
            return response.json()
        except ValueError as exc:
            raise PortalRequestError(
                "The portal response was not valid JSON.",
                status_code=502,
            ) from exc

    except requests.Timeout as exc:
        raise PortalRequestError(
            "The portal request timed out.",
            status_code=504,
        ) from exc

    except requests.HTTPError as exc:
        status_code = (
            exc.response.status_code
            if exc.response is not None
            else 502
        )

        # Preserve the portal's HTTP error status.
        raise PortalRequestError(
            f"Portal returned HTTP {status_code}.",
            status_code=status_code,
        ) from exc

    except requests.RequestException as exc:
        raise PortalRequestError(
            f"Portal request failed: {exc}",
            status_code=502,
        ) from exc
