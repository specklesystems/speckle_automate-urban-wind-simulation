"""This module contains the business logic of the function.

use the automation_context module to wrap your function in an Autamate context helper
"""
import os
import subprocess

from archaea.geometry.vector3d import Vector3d
from archaea.geometry.mesh import Mesh
from archaea_simulation.simulation_objects.domain import Domain
from archaea_simulation.speckle.vtk_to_speckle import vtk_to_speckle
from archaea_simulation.cfd.utils.path import get_cfd_export_path
from pydantic import Field
from speckle_automate import (
    AutomateBase,
    AutomationContext,
    execute_automate_function,
)
from specklepy.api import operations
from specklepy.objects.base import Base
from specklepy.objects.geometry import Brep
from specklepy.transports.server import ServerTransport

from flatten import flatten_base


class FunctionInputs(AutomateBase):
    """These are function author defined values.

    Automate will make sure to supply them matching the types specified here.
    Please use the pydantic model schema to define your inputs:
    https://docs.pydantic.dev/latest/usage/models/
    """

    wind_direction: float = Field(
        title="Wind Direction",
        description=(
            "Wind direction represents as azimuth angle is like a compass direction"
            "with North = 0°, East = 90°, South = 180°, West = 270°."
        ),
    )
    wind_speed: float = Field(
        title="Wind Speed",
        description="Wind speed (m/s) in XY plane."
    )
    number_of_cpus: int = Field(
        title="Number of CPUs",
        description="Number of CPUs to run simulation parallelly.",
        default=4,
    )


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

    print("number of cpus", os.cpu_count())
    subprocess.run("/bin/bash -c 'source /opt/openfoam9/etc/bashrc'", shell=True)
    
    # the context provides a conveniet way, to receive the triggering version
    version_root_object = automate_context.receive_version()
    accepted_types = [Brep.speckle_type]
    objects_to_create_stl = []
    flatten_base_objects = flatten_base(version_root_object)

    count = 0
    for b in flatten_base_objects:
        if b.speckle_type in accepted_types:
            if not b.id:
                raise ValueError("Cannot operate on objects without their id's.")
            
            objects_to_create_stl.append(b)
            # automate_context.add_object_info(
            #     b.id,
            #     "Object included into simulation domain with " f"{b.speckle_type} type."
            # )
            count += 1

    speckle_meshes = []
    for speckle_mesh in objects_to_create_stl:
        speckle_meshes += speckle_mesh.displayValue

    archaea_meshes = []
    for speckle_mesh in speckle_meshes:
        archaea_mesh = Mesh.from_ngon_mesh(speckle_mesh.vertices, speckle_mesh.faces)
        archaea_meshes.append(archaea_mesh)

    # Init domain
    domain = Domain.from_meshes(archaea_meshes, x_scale=5, y_scale=5, z_scale=3, wind_direction=function_inputs.wind_direction, wind_speed=function_inputs.wind_speed)

    # Get folder to copy cases
    archaea_folder = get_cfd_export_path()
    if not os.path.exists(archaea_folder):
        os.makedirs(archaea_folder)

    # Get case folder
    case_folder = os.path.join(archaea_folder, version_root_object.id)
    domain.create_case(case_folder, function_inputs.number_of_cpus)
    cmd_path = os.path.join(case_folder, './Allrun')
    cmd = "/bin/bash -c '{cmd_path}'".format(cmd_path=cmd_path)

    # retcode = subprocess.call(cmd, shell=True, stdout=pipefile)
    completed_process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(completed_process.stdout)

    blockMesh_log = os.path.join(case_folder, 'log.blockMesh')
    add_to_store_if_exist(automate_context, blockMesh_log)

    decomposePar_log = os.path.join(case_folder, 'log.decomposePar')
    add_to_store_if_exist(automate_context, decomposePar_log)
    
    patchSummary_log = os.path.join(case_folder, 'log.patchSummary')
    add_to_store_if_exist(automate_context, patchSummary_log)

    reconstructPar_log = os.path.join(case_folder, 'log.reconstructPar')
    add_to_store_if_exist(automate_context, reconstructPar_log)

    reconstructParMesh_log = os.path.join(case_folder, 'log.reconstructParMesh')
    add_to_store_if_exist(automate_context, reconstructParMesh_log)

    simpleFoam_log = os.path.join(case_folder, 'log.simpleFoam')
    add_to_store_if_exist(automate_context, simpleFoam_log)

    snappyHexMesh_log = os.path.join(case_folder, 'log.snappyHexMesh')
    add_to_store_if_exist(automate_context, snappyHexMesh_log)

    surfaceFeatures_log = os.path.join(case_folder, 'log.surfaceFeatures')
    add_to_store_if_exist(automate_context, surfaceFeatures_log)

    vtk_file = os.path.join(case_folder, 'postProcessing',
                            'cutPlaneSurface', '400', 'U_cutPlane.vtk')
    
    result_mesh = vtk_to_speckle(vtk_file, domain.center.move(Vector3d(domain.x / 2, -domain.y / 2, 0)))

    result = Base()
    result.data = [result_mesh]

    transport = ServerTransport(automate_context.automation_run_data.project_id, automate_context.speckle_client)
    obj_id = operations.send(result, [transport])
    result_branch_name = automate_context.automation_run_data.branch_name + "_result"
    automate_context.speckle_client.branch.create(
        automate_context.automation_run_data.project_id, 
        result_branch_name
        )

    # now create a commit on that branch with your updated data!
    commit_id = automate_context.speckle_client.commit.create(
        automate_context.automation_run_data.project_id,
        obj_id,
        result_branch_name,
        message="Sent from Archaea.",
        source_application='Archaea'
    )

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

def add_to_store_if_exist(automate_context: AutomationContext, path):
    if os.path.exists(path):
        automate_context.store_file_result(path)


# make sure to call the function with the executor
if __name__ == "__main__":
    # NOTE: always pass in the automate function by its reference, do not invoke it!

    # pass in the function reference with the inputs schema to the executor
    execute_automate_function(automate_function, FunctionInputs)

    # if the function has no arguments, the executor can handle it like so
    # execute_automate_function(automate_function_without_inputs)
