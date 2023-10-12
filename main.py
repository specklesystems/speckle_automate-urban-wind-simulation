"""This module contains the business logic of the function.

use the automation_context module to wrap your function in an Autamate context helper
"""

from pydantic import Field
from speckle_automate import (
    AutomateBase,
    AutomationContext,
    execute_automate_function,
)
from specklepy.objects.base import Base
from specklepy.objects.geometry import Box, Brep

from flatten import flatten_base


class FunctionInputs(AutomateBase):
    """These are function author defined values.

    Automate will make sure to supply them matching the types specified here.
    Please use the pydantic model schema to define your inputs:
    https://docs.pydantic.dev/latest/usage/models/
    """

    wind_direction: float
    wind_speed: float


def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs,
) -> None:
    """This is an example Speckle Automate function.

    Args:
        automate_context: A context helper object, that carries relevant information
            about the runtime context of this function.
            It gives access to the Speckle project data, that triggered this run.
            It also has conveniece methods attach result data to the Speckle model.
        function_inputs: An instance object matching the defined schema.
    """
    # the context provides a conveniet way, to receive the triggering version
    version_root_object = automate_context.receive_version()
    accepted_types = [Brep.speckle_type, Box.speckle_type]
    objects_to_create_stl = []

    count = 0
    for b in flatten_base(version_root_object):
        if b.speckle_type in accepted_types:
            if not b.id:
                raise ValueError("Cannot operate on objects without their id's.")
            
            objects_to_create_stl.append(b)
            automate_context.add_object_info(
                b.id,
                "Object included into simulation domain with " f"{b.speckle_type} type."
            )
            count += 1

    if count == 0:
        # this is how a run is marked with a failure cause
        automate_context.mark_run_failed(
            "Automation failed: "
            "Not found appropriate object to run CFD simulation."
        )

    else:
        automate_context.mark_run_success("Object found to run simulation!")

    # if the function generates file results, this is how it can be
    # attached to the Speckle project / model
    # automate_context.store_file_result("./report.pdf")
    # base = Base()
    # automate_context.create_new_version_in_project(base, automate_context.speckle_client.branch.create(automate_context.automation_run_data.project_id, "whatever"))
    # branch_or_error = automate_context.speckle_client.branch.get(automate_context.automation_run_data.project_id, "whatever")

    # We shouldn't create new version under the same model. This will trigger infinite loop -> Don't
    # automate_context.create_new_version_in_project(base, automate_context.automation_run_data.model_id)


# make sure to call the function with the executor
if __name__ == "__main__":
    # NOTE: always pass in the automate function by its reference, do not invoke it!

    # pass in the function reference with the inputs schema to the executor
    execute_automate_function(automate_function, FunctionInputs)

    # if the function has no arguments, the executor can handle it like so
    # execute_automate_function(automate_function_without_inputs)
