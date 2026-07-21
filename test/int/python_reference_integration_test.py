""" python_reference_integration_test.py:

Basic integration tests for the fprime-python reference deployment. These tests exercise the
Python-implemented components (PythonGc, PythonTcpCom, ActiveImager) through the GDS.
"""

from fprime_gds.common.testing_fw import predicates


def test_is_streaming(fprime_test_api):
    """ Test that the flight software is streaming telemetry through the Python communication stack """
    results = fprime_test_api.assert_telemetry_count(5, timeout=10)
    for result in results:
        print(f"received channel {result.get_id()} update: {result.get_str()}")


def test_send_command(fprime_test_api):
    """ Test that commands can be uplinked through the Python communication stack """
    fprime_test_api.send_and_assert_command("CdhCore.cmdDisp.CMD_NO_OP", max_delay=5)
    fprime_test_api.assert_event("CdhCore.cmdDisp.NoOpReceived", timeout=5)


def test_python_gc_telemetry(fprime_test_api):
    """ Test that the PythonGc python component produces telemetry """
    result = fprime_test_api.assert_telemetry(
        "ReferenceDeployment.pythonGc.TrackedObjects", timeout=10
    )
    assert result.get_val() > 0, "PythonGc should track a non-zero number of python objects"
    fprime_test_api.assert_telemetry(
        "ReferenceDeployment.pythonGc.HeldReferences", timeout=10
    )


def test_active_imager_command(fprime_test_api):
    """ Test that the ActiveImager python component handles the TAKE_IMAGE command

    CI machines have no camera, so the component is expected to respond with the
    CameraUnavailable warning event while still completing the command dispatch path.
    """
    fprime_test_api.send_command(
        "ReferenceDeployment.activeImager.TAKE_IMAGE", ["/tmp/test_image.png"]
    )
    event_ids = [
        fprime_test_api.translate_event_name(name)
        for name in (
            "ReferenceDeployment.activeImager.CameraUnavailable",
            "ReferenceDeployment.activeImager.ImagingStart",
        )
    ]
    fprime_test_api.assert_event(predicates.is_a_member_of(event_ids), timeout=10)
