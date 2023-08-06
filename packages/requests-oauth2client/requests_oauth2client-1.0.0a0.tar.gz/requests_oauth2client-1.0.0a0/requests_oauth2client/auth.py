from typing import TYPE_CHECKING, Any, Optional, Union

import requests

from .exceptions import ExpiredAccessToken
from .tokens import BearerToken

if TYPE_CHECKING:  # pragma: no cover
    from .client import OAuth2Client


class BearerAuth(requests.auth.AuthBase):
    """
    A Requests compatible Authentication helper for API protected with Bearer tokens.
    Using this AuthBase, you have to obtain an access token manually.
    """

    def __init__(self, token: Optional[Union[str, BearerToken]] = None) -> None:
        self.token = token  # type: ignore[assignment] # until https://github.com/python/mypy/issues/3004 is fixed

    @property
    def token(self) -> Optional[BearerToken]:
        """
        The token that is used for authorization against the API.
        :return:
        """
        return self._token

    @token.setter
    def token(self, token: Union[str, BearerToken]) -> None:
        if token is not None and not isinstance(token, BearerToken):
            token = BearerToken(token)
        self._token = token

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        if self.token is None:
            return request
        if self.token.is_expired():
            raise ExpiredAccessToken(self.token)
        request.headers["Authorization"] = self.token.authorization_header()
        return request


class OAuth2ClientCredentialsAuth(BearerAuth):
    """
    A Requests Authentication handler that automatically gets access tokens from an OAuth20 Token Endpoint
    with the Client Credentials grant (and can get a new one once it is expired).
    """

    def __init__(self, client: "OAuth2Client", **token_kwargs: Any):
        super().__init__(None)
        self.client = client
        self.token_kwargs = token_kwargs

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        token = self.token
        if token is None or token.is_expired():
            self.token = self.client.client_credentials(**self.token_kwargs)
        return super().__call__(request)


class OAuth2AccessTokenAuth(BearerAuth):
    """
    A Requests Authentication handler using a Bearer access token, and can automatically refreshes it when expired.
    """

    def __init__(
        self,
        client: "OAuth2Client",
        token: Optional[Union[str, BearerToken]] = None,
        **token_kwargs: Any,
    ) -> None:
        """
        Initializes an Authorization handler (RFC6750), with an (optional) initial token.
        :param client: an `OAuth2Client` configured to talk to the token endpoint.
        :param token: a BearerToken that has been retrieved from the token endpoint manually
        :param token_kwargs: additional kwargs to pass to the token endpoint
        """
        super().__init__(token)
        self.client = client
        self.token_kwargs = token_kwargs

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        """
        Adds the
        :param request:
        :return:
        """
        token = self.token
        if (
            token is not None
            and token.is_expired()
            and token.refresh_token
            and self.client is not None
        ):
            self.token = self.client.refresh_token(
                refresh_token=token.refresh_token, **self.token_kwargs
            )
        return super().__call__(request)


class OAuth2AuthorizationCodeAuth(OAuth2AccessTokenAuth):
    """
    A Requests Auth handler that exchanges an Authorization Code for an access token,
    then automatically refreshes it once it is expired.
    """

    def __init__(self, client: "OAuth2Client", code: str, **token_kwargs: Any) -> None:
        super().__init__(client, None)
        self.code: Optional[str] = code
        self.token_kwargs = token_kwargs

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        token = self.token
        if token is None or token.is_expired():
            if self.code:  # pragma: no branch
                self.token = self.client.authorization_code(
                    code=self.code, **self.token_kwargs
                )
                self.code = None
        return super().__call__(request)


class OAuth2DeviceCodeAuth(OAuth2AccessTokenAuth):
    """
    A Requests Auth handler that exchanges a Device Code for an access token,
    then automatically refreshes it once it is expired.
    """

    def __init__(
        self,
        client: "OAuth2Client",
        device_code: str,
        interval: int = 5,
        expires_in: int = 360,
        **token_kwargs: Any,
    ) -> None:
        super().__init__(client, None)
        self.device_code: Optional[str] = device_code
        self.interval = interval
        self.expires_in = expires_in
        self.token_kwargs = token_kwargs

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        from .device_authorization import DeviceAuthorizationPoolingJob

        token = self.token
        if token is None or token.is_expired():
            if self.device_code:  # pragma: no branch
                pooling_job = DeviceAuthorizationPoolingJob(
                    client=self.client,
                    device_code=self.device_code,
                    interval=self.interval,
                )
                while self.token is None:
                    self.token = pooling_job()
                self.device_code = None
        return super().__call__(request)
