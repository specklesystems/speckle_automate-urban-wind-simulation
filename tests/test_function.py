"""Run integration tests with a speckle server."""
import os
import secrets
import string

import pytest
from gql import gql
from speckle_automate import (
    AutomationContext,
    AutomationRunData,
    AutomationStatus,
    run_function,
)
from specklepy.api.client import SpeckleClient
from specklepy.objects.base import Base
from specklepy.transports.server import ServerTransport

from main import FunctionInputs, automate_function


def crypto_random_string(length: int) -> str:
    """Generate a semi crypto random string of a given length."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def register_new_automation(
    project_id: str,
    model_id: str,
    speckle_client: SpeckleClient,
    automation_id: str,
    automation_name: str,
    automation_revision_id: str,
):
    """Register a new automation in the speckle server."""
    query = gql(
        """
        mutation CreateAutomation(
            $projectId: String! 
            $modelId: String! 
            $automationName: String!
            $automationId: String! 
            $automationRevisionId: String!
        ) {
                automationMutations {
                    create(
                        input: {
                            projectId: $projectId
                            modelId: $modelId
                            automationName: $automationName 
                            automationId: $automationId
                            automationRevisionId: $automationRevisionId
                        }
                    )
                }
            }
        """
    )
    params = {
        "projectId": project_id,
        "modelId": model_id,
        "automationName": automation_name,
        "automationId": automation_id,
        "automationRevisionId": automation_revision_id,
    }
    speckle_client.httpclient.execute(query, params)


@pytest.fixture()
def speckle_token() -> str:
    """Provide a speckle token for the test suite."""
    env_var = "SPECKLE_TOKEN"
    token = os.getenv(env_var)
    if not token:
        raise ValueError(f"Cannot run tests without a {env_var} environment variable")
    return token


@pytest.fixture()
def speckle_server_url() -> str:
    """Provide a speckle server url for the test suite, default to localhost."""
    return os.getenv("SPECKLE_SERVER_URL", "http://127.0.0.1:3000")


@pytest.fixture()
def test_client(speckle_server_url: str, speckle_token: str) -> SpeckleClient:
    """Initialize a SpeckleClient for testing."""
    test_client = SpeckleClient(
        speckle_server_url, speckle_server_url.startswith("https")
    )
    test_client.authenticate_with_token(speckle_token)
    return test_client



@pytest.fixture()
def automation_run_data(
    test_client: SpeckleClient, speckle_server_url: str
) -> AutomationRunData:
    """Set up an automation context for testing."""
    project_id: str = "abbc6dc0f7"
    model_name: str = "brep_new"
    version_id: str = "df721bf0c1"
    version_id_2: str = "287887ec10"
    model = test_client.branch.get(project_id, model_name, commits_limit=1)

    model_id: str = model.id

    automation_name = crypto_random_string(10)
    automation_id = crypto_random_string(10)
    automation_revision_id = crypto_random_string(10)

    register_new_automation(
        project_id,
        model_id,
        test_client,
        automation_id,
        automation_name,
        automation_revision_id,
    )

    automation_run_id = crypto_random_string(10)
    function_id = crypto_random_string(10)
    function_release = crypto_random_string(10)
    return AutomationRunData(
        project_id=project_id,
        model_id=model_id,
        branch_name=model_name,
        version_id=version_id_2,
        speckle_server_url=speckle_server_url,
        automation_id=automation_id,
        automation_revision_id=automation_revision_id,
        automation_run_id=automation_run_id,
        function_id=function_id,
        function_name="test",
        function_logo=function_release,
    )


def test_function_run(automation_run_data: AutomationRunData, speckle_token: str):
    """Run an integration test for the automate function."""
    automate_sdk = run_function(
        AutomationContext.initialize(automation_run_data, speckle_token),
        automate_function,
        FunctionInputs(wind_speed=10, wind_direction=45, number_of_cpus=6),
    )

    assert automate_sdk.run_status == AutomationStatus.FAILED
