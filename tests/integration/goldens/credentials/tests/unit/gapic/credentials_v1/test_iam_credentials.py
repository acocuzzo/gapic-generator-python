# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

import grpc
from grpc.experimental import aio
from collections.abc import Iterable
from google.protobuf import json_format
import json
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule
from proto.marshal.rules import wrappers
from requests import Response
from requests import Request, PreparedRequest
from requests.sessions import Session
from google.protobuf import json_format

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.iam.credentials_v1.services.iam_credentials import IAMCredentialsAsyncClient
from google.iam.credentials_v1.services.iam_credentials import IAMCredentialsClient
from google.iam.credentials_v1.services.iam_credentials import transports
from google.iam.credentials_v1.types import common
from google.oauth2 import service_account
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return "foo.googleapis.com" if ("localhost" in client.DEFAULT_ENDPOINT) else client.DEFAULT_ENDPOINT


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert IAMCredentialsClient._get_default_mtls_endpoint(None) is None
    assert IAMCredentialsClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert IAMCredentialsClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert IAMCredentialsClient._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert IAMCredentialsClient._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert IAMCredentialsClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class,transport_name", [
    (IAMCredentialsClient, "grpc"),
    (IAMCredentialsAsyncClient, "grpc_asyncio"),
    (IAMCredentialsClient, "rest"),
])
def test_iam_credentials_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_info') as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'iamcredentials.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://iamcredentials.googleapis.com'
        )


@pytest.mark.parametrize("transport_class,transport_name", [
    (transports.IAMCredentialsGrpcTransport, "grpc"),
    (transports.IAMCredentialsGrpcAsyncIOTransport, "grpc_asyncio"),
    (transports.IAMCredentialsRestTransport, "rest"),
])
def test_iam_credentials_client_service_account_always_use_jwt(transport_class, transport_name):
    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class,transport_name", [
    (IAMCredentialsClient, "grpc"),
    (IAMCredentialsAsyncClient, "grpc_asyncio"),
    (IAMCredentialsClient, "rest"),
])
def test_iam_credentials_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_file') as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'iamcredentials.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://iamcredentials.googleapis.com'
        )


def test_iam_credentials_client_get_transport_class():
    transport = IAMCredentialsClient.get_transport_class()
    available_transports = [
        transports.IAMCredentialsGrpcTransport,
        transports.IAMCredentialsRestTransport,
    ]
    assert transport in available_transports

    transport = IAMCredentialsClient.get_transport_class("grpc")
    assert transport == transports.IAMCredentialsGrpcTransport


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (IAMCredentialsClient, transports.IAMCredentialsGrpcTransport, "grpc"),
    (IAMCredentialsAsyncClient, transports.IAMCredentialsGrpcAsyncIOTransport, "grpc_asyncio"),
    (IAMCredentialsClient, transports.IAMCredentialsRestTransport, "rest"),
])
@mock.patch.object(IAMCredentialsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(IAMCredentialsClient))
@mock.patch.object(IAMCredentialsAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(IAMCredentialsAsyncClient))
def test_iam_credentials_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(IAMCredentialsClient, 'get_transport_class') as gtc:
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials()
        )
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(IAMCredentialsClient, 'get_transport_class') as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(api_audience="https://language.googleapis.com")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com"
        )

@pytest.mark.parametrize("client_class,transport_class,transport_name,use_client_cert_env", [
    (IAMCredentialsClient, transports.IAMCredentialsGrpcTransport, "grpc", "true"),
    (IAMCredentialsAsyncClient, transports.IAMCredentialsGrpcAsyncIOTransport, "grpc_asyncio", "true"),
    (IAMCredentialsClient, transports.IAMCredentialsGrpcTransport, "grpc", "false"),
    (IAMCredentialsAsyncClient, transports.IAMCredentialsGrpcAsyncIOTransport, "grpc_asyncio", "false"),
    (IAMCredentialsClient, transports.IAMCredentialsRestTransport, "rest", "true"),
    (IAMCredentialsClient, transports.IAMCredentialsRestTransport, "rest", "false"),
])
@mock.patch.object(IAMCredentialsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(IAMCredentialsClient))
@mock.patch.object(IAMCredentialsAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(IAMCredentialsAsyncClient))
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_iam_credentials_client_mtls_env_auto(client_class, transport_class, transport_name, use_client_cert_env):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        options = client_options.ClientOptions(client_cert_source=client_cert_source_callback)
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
                with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=client_cert_source_callback):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch("google.auth.transport.mtls.has_default_client_cert_source", return_value=False):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [
    IAMCredentialsClient, IAMCredentialsAsyncClient
])
@mock.patch.object(IAMCredentialsClient, "DEFAULT_ENDPOINT", modify_default_endpoint(IAMCredentialsClient))
@mock.patch.object(IAMCredentialsAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(IAMCredentialsAsyncClient))
def test_iam_credentials_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=False):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
            with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=mock_client_cert_source):
                api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (IAMCredentialsClient, transports.IAMCredentialsGrpcTransport, "grpc"),
    (IAMCredentialsAsyncClient, transports.IAMCredentialsGrpcAsyncIOTransport, "grpc_asyncio"),
    (IAMCredentialsClient, transports.IAMCredentialsRestTransport, "rest"),
])
def test_iam_credentials_client_client_options_scopes(client_class, transport_class, transport_name):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (IAMCredentialsClient, transports.IAMCredentialsGrpcTransport, "grpc", grpc_helpers),
    (IAMCredentialsAsyncClient, transports.IAMCredentialsGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
    (IAMCredentialsClient, transports.IAMCredentialsRestTransport, "rest", None),
])
def test_iam_credentials_client_client_options_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

def test_iam_credentials_client_client_options_from_dict():
    with mock.patch('google.iam.credentials_v1.services.iam_credentials.transports.IAMCredentialsGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = IAMCredentialsClient(
            client_options={'api_endpoint': 'squid.clam.whelk'}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (IAMCredentialsClient, transports.IAMCredentialsGrpcTransport, "grpc", grpc_helpers),
    (IAMCredentialsAsyncClient, transports.IAMCredentialsGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
])
def test_iam_credentials_client_create_channel_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "iamcredentials.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
),
            scopes=None,
            default_host="iamcredentials.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("request_type", [
  common.GenerateAccessTokenRequest,
  dict,
])
def test_generate_access_token(request_type, transport: str = 'grpc'):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_access_token),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.GenerateAccessTokenResponse(
            access_token='access_token_value',
        )
        response = client.generate_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == common.GenerateAccessTokenRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.GenerateAccessTokenResponse)
    assert response.access_token == 'access_token_value'


def test_generate_access_token_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_access_token),
            '__call__') as call:
        client.generate_access_token()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == common.GenerateAccessTokenRequest()

@pytest.mark.asyncio
async def test_generate_access_token_async(transport: str = 'grpc_asyncio', request_type=common.GenerateAccessTokenRequest):
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_access_token),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(common.GenerateAccessTokenResponse(
            access_token='access_token_value',
        ))
        response = await client.generate_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == common.GenerateAccessTokenRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.GenerateAccessTokenResponse)
    assert response.access_token == 'access_token_value'


@pytest.mark.asyncio
async def test_generate_access_token_async_from_dict():
    await test_generate_access_token_async(request_type=dict)


def test_generate_access_token_field_headers():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = common.GenerateAccessTokenRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_access_token),
            '__call__') as call:
        call.return_value = common.GenerateAccessTokenResponse()
        client.generate_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_generate_access_token_field_headers_async():
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = common.GenerateAccessTokenRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_access_token),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(common.GenerateAccessTokenResponse())
        await client.generate_access_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_generate_access_token_flattened():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_access_token),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.GenerateAccessTokenResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.generate_access_token(
            name='name_value',
            delegates=['delegates_value'],
            scope=['scope_value'],
            lifetime=duration_pb2.Duration(seconds=751),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].delegates
        mock_val = ['delegates_value']
        assert arg == mock_val
        arg = args[0].scope
        mock_val = ['scope_value']
        assert arg == mock_val
        assert DurationRule().to_proto(args[0].lifetime) == duration_pb2.Duration(seconds=751)


def test_generate_access_token_flattened_error():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_access_token(
            common.GenerateAccessTokenRequest(),
            name='name_value',
            delegates=['delegates_value'],
            scope=['scope_value'],
            lifetime=duration_pb2.Duration(seconds=751),
        )

@pytest.mark.asyncio
async def test_generate_access_token_flattened_async():
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_access_token),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.GenerateAccessTokenResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(common.GenerateAccessTokenResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.generate_access_token(
            name='name_value',
            delegates=['delegates_value'],
            scope=['scope_value'],
            lifetime=duration_pb2.Duration(seconds=751),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].delegates
        mock_val = ['delegates_value']
        assert arg == mock_val
        arg = args[0].scope
        mock_val = ['scope_value']
        assert arg == mock_val
        assert DurationRule().to_proto(args[0].lifetime) == duration_pb2.Duration(seconds=751)

@pytest.mark.asyncio
async def test_generate_access_token_flattened_error_async():
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.generate_access_token(
            common.GenerateAccessTokenRequest(),
            name='name_value',
            delegates=['delegates_value'],
            scope=['scope_value'],
            lifetime=duration_pb2.Duration(seconds=751),
        )


@pytest.mark.parametrize("request_type", [
  common.GenerateIdTokenRequest,
  dict,
])
def test_generate_id_token(request_type, transport: str = 'grpc'):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_id_token),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.GenerateIdTokenResponse(
            token='token_value',
        )
        response = client.generate_id_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == common.GenerateIdTokenRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.GenerateIdTokenResponse)
    assert response.token == 'token_value'


def test_generate_id_token_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_id_token),
            '__call__') as call:
        client.generate_id_token()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == common.GenerateIdTokenRequest()

@pytest.mark.asyncio
async def test_generate_id_token_async(transport: str = 'grpc_asyncio', request_type=common.GenerateIdTokenRequest):
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_id_token),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(common.GenerateIdTokenResponse(
            token='token_value',
        ))
        response = await client.generate_id_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == common.GenerateIdTokenRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.GenerateIdTokenResponse)
    assert response.token == 'token_value'


@pytest.mark.asyncio
async def test_generate_id_token_async_from_dict():
    await test_generate_id_token_async(request_type=dict)


def test_generate_id_token_field_headers():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = common.GenerateIdTokenRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_id_token),
            '__call__') as call:
        call.return_value = common.GenerateIdTokenResponse()
        client.generate_id_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_generate_id_token_field_headers_async():
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = common.GenerateIdTokenRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_id_token),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(common.GenerateIdTokenResponse())
        await client.generate_id_token(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_generate_id_token_flattened():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_id_token),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.GenerateIdTokenResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.generate_id_token(
            name='name_value',
            delegates=['delegates_value'],
            audience='audience_value',
            include_email=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].delegates
        mock_val = ['delegates_value']
        assert arg == mock_val
        arg = args[0].audience
        mock_val = 'audience_value'
        assert arg == mock_val
        arg = args[0].include_email
        mock_val = True
        assert arg == mock_val


def test_generate_id_token_flattened_error():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_id_token(
            common.GenerateIdTokenRequest(),
            name='name_value',
            delegates=['delegates_value'],
            audience='audience_value',
            include_email=True,
        )

@pytest.mark.asyncio
async def test_generate_id_token_flattened_async():
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.generate_id_token),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.GenerateIdTokenResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(common.GenerateIdTokenResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.generate_id_token(
            name='name_value',
            delegates=['delegates_value'],
            audience='audience_value',
            include_email=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].delegates
        mock_val = ['delegates_value']
        assert arg == mock_val
        arg = args[0].audience
        mock_val = 'audience_value'
        assert arg == mock_val
        arg = args[0].include_email
        mock_val = True
        assert arg == mock_val

@pytest.mark.asyncio
async def test_generate_id_token_flattened_error_async():
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.generate_id_token(
            common.GenerateIdTokenRequest(),
            name='name_value',
            delegates=['delegates_value'],
            audience='audience_value',
            include_email=True,
        )


@pytest.mark.parametrize("request_type", [
  common.SignBlobRequest,
  dict,
])
def test_sign_blob(request_type, transport: str = 'grpc'):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_blob),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.SignBlobResponse(
            key_id='key_id_value',
            signed_blob=b'signed_blob_blob',
        )
        response = client.sign_blob(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == common.SignBlobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.SignBlobResponse)
    assert response.key_id == 'key_id_value'
    assert response.signed_blob == b'signed_blob_blob'


def test_sign_blob_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_blob),
            '__call__') as call:
        client.sign_blob()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == common.SignBlobRequest()

@pytest.mark.asyncio
async def test_sign_blob_async(transport: str = 'grpc_asyncio', request_type=common.SignBlobRequest):
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_blob),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(common.SignBlobResponse(
            key_id='key_id_value',
            signed_blob=b'signed_blob_blob',
        ))
        response = await client.sign_blob(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == common.SignBlobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.SignBlobResponse)
    assert response.key_id == 'key_id_value'
    assert response.signed_blob == b'signed_blob_blob'


@pytest.mark.asyncio
async def test_sign_blob_async_from_dict():
    await test_sign_blob_async(request_type=dict)


def test_sign_blob_field_headers():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = common.SignBlobRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_blob),
            '__call__') as call:
        call.return_value = common.SignBlobResponse()
        client.sign_blob(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_sign_blob_field_headers_async():
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = common.SignBlobRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_blob),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(common.SignBlobResponse())
        await client.sign_blob(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_sign_blob_flattened():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_blob),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.SignBlobResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.sign_blob(
            name='name_value',
            delegates=['delegates_value'],
            payload=b'payload_blob',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].delegates
        mock_val = ['delegates_value']
        assert arg == mock_val
        arg = args[0].payload
        mock_val = b'payload_blob'
        assert arg == mock_val


def test_sign_blob_flattened_error():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.sign_blob(
            common.SignBlobRequest(),
            name='name_value',
            delegates=['delegates_value'],
            payload=b'payload_blob',
        )

@pytest.mark.asyncio
async def test_sign_blob_flattened_async():
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_blob),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.SignBlobResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(common.SignBlobResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.sign_blob(
            name='name_value',
            delegates=['delegates_value'],
            payload=b'payload_blob',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].delegates
        mock_val = ['delegates_value']
        assert arg == mock_val
        arg = args[0].payload
        mock_val = b'payload_blob'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_sign_blob_flattened_error_async():
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.sign_blob(
            common.SignBlobRequest(),
            name='name_value',
            delegates=['delegates_value'],
            payload=b'payload_blob',
        )


@pytest.mark.parametrize("request_type", [
  common.SignJwtRequest,
  dict,
])
def test_sign_jwt(request_type, transport: str = 'grpc'):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_jwt),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.SignJwtResponse(
            key_id='key_id_value',
            signed_jwt='signed_jwt_value',
        )
        response = client.sign_jwt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == common.SignJwtRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.SignJwtResponse)
    assert response.key_id == 'key_id_value'
    assert response.signed_jwt == 'signed_jwt_value'


def test_sign_jwt_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_jwt),
            '__call__') as call:
        client.sign_jwt()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == common.SignJwtRequest()

@pytest.mark.asyncio
async def test_sign_jwt_async(transport: str = 'grpc_asyncio', request_type=common.SignJwtRequest):
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_jwt),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(common.SignJwtResponse(
            key_id='key_id_value',
            signed_jwt='signed_jwt_value',
        ))
        response = await client.sign_jwt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == common.SignJwtRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.SignJwtResponse)
    assert response.key_id == 'key_id_value'
    assert response.signed_jwt == 'signed_jwt_value'


@pytest.mark.asyncio
async def test_sign_jwt_async_from_dict():
    await test_sign_jwt_async(request_type=dict)


def test_sign_jwt_field_headers():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = common.SignJwtRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_jwt),
            '__call__') as call:
        call.return_value = common.SignJwtResponse()
        client.sign_jwt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_sign_jwt_field_headers_async():
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = common.SignJwtRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_jwt),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(common.SignJwtResponse())
        await client.sign_jwt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_sign_jwt_flattened():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_jwt),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.SignJwtResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.sign_jwt(
            name='name_value',
            delegates=['delegates_value'],
            payload='payload_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].delegates
        mock_val = ['delegates_value']
        assert arg == mock_val
        arg = args[0].payload
        mock_val = 'payload_value'
        assert arg == mock_val


def test_sign_jwt_flattened_error():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.sign_jwt(
            common.SignJwtRequest(),
            name='name_value',
            delegates=['delegates_value'],
            payload='payload_value',
        )

@pytest.mark.asyncio
async def test_sign_jwt_flattened_async():
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.sign_jwt),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.SignJwtResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(common.SignJwtResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.sign_jwt(
            name='name_value',
            delegates=['delegates_value'],
            payload='payload_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val
        arg = args[0].delegates
        mock_val = ['delegates_value']
        assert arg == mock_val
        arg = args[0].payload
        mock_val = 'payload_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_sign_jwt_flattened_error_async():
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.sign_jwt(
            common.SignJwtRequest(),
            name='name_value',
            delegates=['delegates_value'],
            payload='payload_value',
        )


@pytest.mark.parametrize("request_type", [
    common.GenerateAccessTokenRequest,
    dict,
])
def test_generate_access_token_rest(request_type):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/serviceAccounts/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = common.GenerateAccessTokenResponse(
              access_token='access_token_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = common.GenerateAccessTokenResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.generate_access_token(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.GenerateAccessTokenResponse)
    assert response.access_token == 'access_token_value'


def test_generate_access_token_rest_required_fields(request_type=common.GenerateAccessTokenRequest):
    transport_class = transports.IAMCredentialsRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["scope"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).generate_access_token._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'
    jsonified_request["scope"] = 'scope_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).generate_access_token._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'
    assert "scope" in jsonified_request
    assert jsonified_request["scope"] == 'scope_value'

    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = common.GenerateAccessTokenResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = common.GenerateAccessTokenResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.generate_access_token(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_generate_access_token_rest_unset_required_fields():
    transport = transports.IAMCredentialsRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.generate_access_token._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", "scope", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_generate_access_token_rest_interceptors(null_interceptor):
    transport = transports.IAMCredentialsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.IAMCredentialsRestInterceptor(),
        )
    client = IAMCredentialsClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.IAMCredentialsRestInterceptor, "post_generate_access_token") as post, \
         mock.patch.object(transports.IAMCredentialsRestInterceptor, "pre_generate_access_token") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = common.GenerateAccessTokenRequest.pb(common.GenerateAccessTokenRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = common.GenerateAccessTokenResponse.to_json(common.GenerateAccessTokenResponse())

        request = common.GenerateAccessTokenRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = common.GenerateAccessTokenResponse()

        client.generate_access_token(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_generate_access_token_rest_bad_request(transport: str = 'rest', request_type=common.GenerateAccessTokenRequest):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/serviceAccounts/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.generate_access_token(request)


def test_generate_access_token_rest_flattened():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = common.GenerateAccessTokenResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/serviceAccounts/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
            delegates=['delegates_value'],
            scope=['scope_value'],
            lifetime=duration_pb2.Duration(seconds=751),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = common.GenerateAccessTokenResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.generate_access_token(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/serviceAccounts/*}:generateAccessToken" % client.transport._host, args[1])


def test_generate_access_token_rest_flattened_error(transport: str = 'rest'):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_access_token(
            common.GenerateAccessTokenRequest(),
            name='name_value',
            delegates=['delegates_value'],
            scope=['scope_value'],
            lifetime=duration_pb2.Duration(seconds=751),
        )


def test_generate_access_token_rest_error():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    common.GenerateIdTokenRequest,
    dict,
])
def test_generate_id_token_rest(request_type):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/serviceAccounts/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = common.GenerateIdTokenResponse(
              token='token_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = common.GenerateIdTokenResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.generate_id_token(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.GenerateIdTokenResponse)
    assert response.token == 'token_value'


def test_generate_id_token_rest_required_fields(request_type=common.GenerateIdTokenRequest):
    transport_class = transports.IAMCredentialsRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["audience"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).generate_id_token._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'
    jsonified_request["audience"] = 'audience_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).generate_id_token._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'
    assert "audience" in jsonified_request
    assert jsonified_request["audience"] == 'audience_value'

    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = common.GenerateIdTokenResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = common.GenerateIdTokenResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.generate_id_token(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_generate_id_token_rest_unset_required_fields():
    transport = transports.IAMCredentialsRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.generate_id_token._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", "audience", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_generate_id_token_rest_interceptors(null_interceptor):
    transport = transports.IAMCredentialsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.IAMCredentialsRestInterceptor(),
        )
    client = IAMCredentialsClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.IAMCredentialsRestInterceptor, "post_generate_id_token") as post, \
         mock.patch.object(transports.IAMCredentialsRestInterceptor, "pre_generate_id_token") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = common.GenerateIdTokenRequest.pb(common.GenerateIdTokenRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = common.GenerateIdTokenResponse.to_json(common.GenerateIdTokenResponse())

        request = common.GenerateIdTokenRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = common.GenerateIdTokenResponse()

        client.generate_id_token(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_generate_id_token_rest_bad_request(transport: str = 'rest', request_type=common.GenerateIdTokenRequest):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/serviceAccounts/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.generate_id_token(request)


def test_generate_id_token_rest_flattened():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = common.GenerateIdTokenResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/serviceAccounts/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
            delegates=['delegates_value'],
            audience='audience_value',
            include_email=True,
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = common.GenerateIdTokenResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.generate_id_token(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/serviceAccounts/*}:generateIdToken" % client.transport._host, args[1])


def test_generate_id_token_rest_flattened_error(transport: str = 'rest'):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.generate_id_token(
            common.GenerateIdTokenRequest(),
            name='name_value',
            delegates=['delegates_value'],
            audience='audience_value',
            include_email=True,
        )


def test_generate_id_token_rest_error():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    common.SignBlobRequest,
    dict,
])
def test_sign_blob_rest(request_type):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/serviceAccounts/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = common.SignBlobResponse(
              key_id='key_id_value',
              signed_blob=b'signed_blob_blob',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = common.SignBlobResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.sign_blob(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.SignBlobResponse)
    assert response.key_id == 'key_id_value'
    assert response.signed_blob == b'signed_blob_blob'


def test_sign_blob_rest_required_fields(request_type=common.SignBlobRequest):
    transport_class = transports.IAMCredentialsRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["payload"] = b''
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).sign_blob._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'
    jsonified_request["payload"] = b'payload_blob'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).sign_blob._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'
    assert "payload" in jsonified_request
    assert jsonified_request["payload"] == b'payload_blob'

    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = common.SignBlobResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = common.SignBlobResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.sign_blob(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_sign_blob_rest_unset_required_fields():
    transport = transports.IAMCredentialsRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.sign_blob._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", "payload", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_sign_blob_rest_interceptors(null_interceptor):
    transport = transports.IAMCredentialsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.IAMCredentialsRestInterceptor(),
        )
    client = IAMCredentialsClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.IAMCredentialsRestInterceptor, "post_sign_blob") as post, \
         mock.patch.object(transports.IAMCredentialsRestInterceptor, "pre_sign_blob") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = common.SignBlobRequest.pb(common.SignBlobRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = common.SignBlobResponse.to_json(common.SignBlobResponse())

        request = common.SignBlobRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = common.SignBlobResponse()

        client.sign_blob(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_sign_blob_rest_bad_request(transport: str = 'rest', request_type=common.SignBlobRequest):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/serviceAccounts/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.sign_blob(request)


def test_sign_blob_rest_flattened():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = common.SignBlobResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/serviceAccounts/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
            delegates=['delegates_value'],
            payload=b'payload_blob',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = common.SignBlobResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.sign_blob(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/serviceAccounts/*}:signBlob" % client.transport._host, args[1])


def test_sign_blob_rest_flattened_error(transport: str = 'rest'):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.sign_blob(
            common.SignBlobRequest(),
            name='name_value',
            delegates=['delegates_value'],
            payload=b'payload_blob',
        )


def test_sign_blob_rest_error():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    common.SignJwtRequest,
    dict,
])
def test_sign_jwt_rest(request_type):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/serviceAccounts/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = common.SignJwtResponse(
              key_id='key_id_value',
              signed_jwt='signed_jwt_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = common.SignJwtResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.sign_jwt(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.SignJwtResponse)
    assert response.key_id == 'key_id_value'
    assert response.signed_jwt == 'signed_jwt_value'


def test_sign_jwt_rest_required_fields(request_type=common.SignJwtRequest):
    transport_class = transports.IAMCredentialsRestTransport

    request_init = {}
    request_init["name"] = ""
    request_init["payload"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).sign_jwt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'
    jsonified_request["payload"] = 'payload_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).sign_jwt._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'
    assert "payload" in jsonified_request
    assert jsonified_request["payload"] == 'payload_value'

    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = common.SignJwtResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            # Convert return value to protobuf type
            return_value = common.SignJwtResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.sign_jwt(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_sign_jwt_rest_unset_required_fields():
    transport = transports.IAMCredentialsRestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.sign_jwt._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", "payload", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_sign_jwt_rest_interceptors(null_interceptor):
    transport = transports.IAMCredentialsRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.IAMCredentialsRestInterceptor(),
        )
    client = IAMCredentialsClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.IAMCredentialsRestInterceptor, "post_sign_jwt") as post, \
         mock.patch.object(transports.IAMCredentialsRestInterceptor, "pre_sign_jwt") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = common.SignJwtRequest.pb(common.SignJwtRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = common.SignJwtResponse.to_json(common.SignJwtResponse())

        request = common.SignJwtRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = common.SignJwtResponse()

        client.sign_jwt(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_sign_jwt_rest_bad_request(transport: str = 'rest', request_type=common.SignJwtRequest):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/serviceAccounts/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.sign_jwt(request)


def test_sign_jwt_rest_flattened():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = common.SignJwtResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/serviceAccounts/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
            delegates=['delegates_value'],
            payload='payload_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        # Convert return value to protobuf type
        return_value = common.SignJwtResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.sign_jwt(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/serviceAccounts/*}:signJwt" % client.transport._host, args[1])


def test_sign_jwt_rest_flattened_error(transport: str = 'rest'):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.sign_jwt(
            common.SignJwtRequest(),
            name='name_value',
            delegates=['delegates_value'],
            payload='payload_value',
        )


def test_sign_jwt_rest_error():
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.IAMCredentialsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = IAMCredentialsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.IAMCredentialsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = IAMCredentialsClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.IAMCredentialsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = IAMCredentialsClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = IAMCredentialsClient(
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.IAMCredentialsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = IAMCredentialsClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.IAMCredentialsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = IAMCredentialsClient(transport=transport)
    assert client.transport is transport

def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.IAMCredentialsGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.IAMCredentialsGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

@pytest.mark.parametrize("transport_class", [
    transports.IAMCredentialsGrpcTransport,
    transports.IAMCredentialsGrpcAsyncIOTransport,
    transports.IAMCredentialsRestTransport,
])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, 'default') as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "rest",
])
def test_transport_kind(transport_name):
    transport = IAMCredentialsClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name

def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.IAMCredentialsGrpcTransport,
    )

def test_iam_credentials_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.IAMCredentialsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json"
        )


def test_iam_credentials_base_transport():
    # Instantiate the base transport.
    with mock.patch('google.iam.credentials_v1.services.iam_credentials.transports.IAMCredentialsTransport.__init__') as Transport:
        Transport.return_value = None
        transport = transports.IAMCredentialsTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'generate_access_token',
        'generate_id_token',
        'sign_blob',
        'sign_jwt',
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Catch all for all remaining methods and properties
    remainder = [
        'kind',
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_iam_credentials_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(google.auth, 'load_credentials_from_file', autospec=True) as load_creds, mock.patch('google.iam.credentials_v1.services.iam_credentials.transports.IAMCredentialsTransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.IAMCredentialsTransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with("credentials.json",
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
),
            quota_project_id="octopus",
        )


def test_iam_credentials_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc, mock.patch('google.iam.credentials_v1.services.iam_credentials.transports.IAMCredentialsTransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.IAMCredentialsTransport()
        adc.assert_called_once()


def test_iam_credentials_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        IAMCredentialsClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.IAMCredentialsGrpcTransport,
        transports.IAMCredentialsGrpcAsyncIOTransport,
    ],
)
def test_iam_credentials_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(                'https://www.googleapis.com/auth/cloud-platform',),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.IAMCredentialsGrpcTransport,
        transports.IAMCredentialsGrpcAsyncIOTransport,
        transports.IAMCredentialsRestTransport,
    ],
)
def test_iam_credentials_transport_auth_gdch_credentials(transport_class):
    host = 'https://language.com'
    api_audience_tests = [None, 'https://language2.com']
    api_audience_expect = [host, 'https://language2.com']
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, 'default', autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(return_value=gdch_mock)
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(
                e
            )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.IAMCredentialsGrpcTransport, grpc_helpers),
        (transports.IAMCredentialsGrpcAsyncIOTransport, grpc_helpers_async)
    ],
)
def test_iam_credentials_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(
            quota_project_id="octopus",
            scopes=["1", "2"]
        )

        create_channel.assert_called_with(
            "iamcredentials.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
),
            scopes=["1", "2"],
            default_host="iamcredentials.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("transport_class", [transports.IAMCredentialsGrpcTransport, transports.IAMCredentialsGrpcAsyncIOTransport])
def test_iam_credentials_grpc_transport_client_cert_source_for_mtls(
    transport_class
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert,
                private_key=expected_key
            )

def test_iam_credentials_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch("google.auth.transport.requests.AuthorizedSession.configure_mtls_channel") as mock_configure_mtls_channel:
        transports.IAMCredentialsRestTransport (
            credentials=cred,
            client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_iam_credentials_host_no_port(transport_name):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='iamcredentials.googleapis.com'),
         transport=transport_name,
    )
    assert client.transport._host == (
        'iamcredentials.googleapis.com:443'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://iamcredentials.googleapis.com'
    )

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_iam_credentials_host_with_port(transport_name):
    client = IAMCredentialsClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='iamcredentials.googleapis.com:8000'),
        transport=transport_name,
    )
    assert client.transport._host == (
        'iamcredentials.googleapis.com:8000'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://iamcredentials.googleapis.com:8000'
    )

@pytest.mark.parametrize("transport_name", [
    "rest",
])
def test_iam_credentials_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = IAMCredentialsClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = IAMCredentialsClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.generate_access_token._session
    session2 = client2.transport.generate_access_token._session
    assert session1 != session2
    session1 = client1.transport.generate_id_token._session
    session2 = client2.transport.generate_id_token._session
    assert session1 != session2
    session1 = client1.transport.sign_blob._session
    session2 = client2.transport.sign_blob._session
    assert session1 != session2
    session1 = client1.transport.sign_jwt._session
    session2 = client2.transport.sign_jwt._session
    assert session1 != session2
def test_iam_credentials_grpc_transport_channel():
    channel = grpc.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.IAMCredentialsGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_iam_credentials_grpc_asyncio_transport_channel():
    channel = aio.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.IAMCredentialsGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.IAMCredentialsGrpcTransport, transports.IAMCredentialsGrpcAsyncIOTransport])
def test_iam_credentials_transport_channel_mtls_with_client_cert_source(
    transport_class
):
    with mock.patch("grpc.ssl_channel_credentials", autospec=True) as grpc_ssl_channel_cred:
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, 'default') as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.IAMCredentialsGrpcTransport, transports.IAMCredentialsGrpcAsyncIOTransport])
def test_iam_credentials_transport_channel_mtls_with_adc(
    transport_class
):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_service_account_path():
    project = "squid"
    service_account = "clam"
    expected = "projects/{project}/serviceAccounts/{service_account}".format(project=project, service_account=service_account, )
    actual = IAMCredentialsClient.service_account_path(project, service_account)
    assert expected == actual


def test_parse_service_account_path():
    expected = {
        "project": "whelk",
        "service_account": "octopus",
    }
    path = IAMCredentialsClient.service_account_path(**expected)

    # Check that the path construction is reversible.
    actual = IAMCredentialsClient.parse_service_account_path(path)
    assert expected == actual

def test_common_billing_account_path():
    billing_account = "oyster"
    expected = "billingAccounts/{billing_account}".format(billing_account=billing_account, )
    actual = IAMCredentialsClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = IAMCredentialsClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = IAMCredentialsClient.parse_common_billing_account_path(path)
    assert expected == actual

def test_common_folder_path():
    folder = "cuttlefish"
    expected = "folders/{folder}".format(folder=folder, )
    actual = IAMCredentialsClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = IAMCredentialsClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = IAMCredentialsClient.parse_common_folder_path(path)
    assert expected == actual

def test_common_organization_path():
    organization = "winkle"
    expected = "organizations/{organization}".format(organization=organization, )
    actual = IAMCredentialsClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = IAMCredentialsClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = IAMCredentialsClient.parse_common_organization_path(path)
    assert expected == actual

def test_common_project_path():
    project = "scallop"
    expected = "projects/{project}".format(project=project, )
    actual = IAMCredentialsClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = IAMCredentialsClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = IAMCredentialsClient.parse_common_project_path(path)
    assert expected == actual

def test_common_location_path():
    project = "squid"
    location = "clam"
    expected = "projects/{project}/locations/{location}".format(project=project, location=location, )
    actual = IAMCredentialsClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = IAMCredentialsClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = IAMCredentialsClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(transports.IAMCredentialsTransport, '_prep_wrapped_messages') as prep:
        client = IAMCredentialsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(transports.IAMCredentialsTransport, '_prep_wrapped_messages') as prep:
        transport_class = IAMCredentialsClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

@pytest.mark.asyncio
async def test_transport_close_async():
    client = IAMCredentialsAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(type(getattr(client.transport, "grpc_channel")), "close") as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = IAMCredentialsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        with mock.patch.object(type(getattr(client.transport, close_name)), "close") as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()

def test_client_ctx():
    transports = [
        'rest',
        'grpc',
    ]
    for transport in transports:
        client = IAMCredentialsClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()

@pytest.mark.parametrize("client_class,transport_class", [
    (IAMCredentialsClient, transports.IAMCredentialsGrpcTransport),
    (IAMCredentialsAsyncClient, transports.IAMCredentialsGrpcAsyncIOTransport),
])
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
