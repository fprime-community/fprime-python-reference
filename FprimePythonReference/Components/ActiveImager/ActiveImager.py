""" ActiveImager Python component implementation

This is the Python implementation for the ActiveImager component. This class extends the auto-coded python base
class ActiveImagerBase that provides the necessary plumbing to connect to the C++ stub connected to the rest of
the F Prime topology.
"""
import fprime_py
from ActiveImagerBaseAc import ActiveImagerBase

import cv2
from pathlib import Path

CAMERA_INDEX = 0

class ActiveImager(ActiveImagerBase):
    """ Python implementation for the ActiveImager component """
    def __init__(self):
        """ Construct the component
        
        The component is constructed during the "init" phase when the component is originally called. During this phase
        the F Prime topology is not yet fully constructed, so only basic initialization should be done here.
        """
        super().__init__()
        self.capture = None

    def open_camera(self):
        """ Open the camera capture object if possible

        Returns the opened cv2.VideoCapture object, or None when no camera is available. The capture object is
        opened lazily and cached so repeated commands reuse the same camera handle, keeping camera-less systems
        (e.g. CI machines) from failing at component construction time.
        """
        if self.capture is not None and self.capture.isOpened():
            return self.capture
        self.capture = None
        try:
            capture = cv2.VideoCapture(CAMERA_INDEX)
            if not capture.isOpened():
                capture.release()
                raise cv2.error(f"camera {CAMERA_INDEX} failed to open")
            self.capture = capture
        except cv2.error as exc:
            print(f"[WARNING] Camera is not available: {exc}")
            self.log_WARNING_HI_CameraUnavailable()
        return self.capture

    def TAKE_IMAGE_cmdHandler(self, opCode, cmdSeq, string_argument):
        """ Handle the TAKE_IMAGE command """
        return_status = fprime_py.Fw.CmdResponse.T.OK
        # Check for camera availability
        if self.open_camera() is None:
            return_status = fprime_py.Fw.CmdResponse.T.EXECUTION_ERROR
        else:
            # Start imaging process
            self.log_ACTIVITY_HI_ImagingStart()
            returned_status, returned_frame = self.capture.read()
            if returned_status:
                try:
                    cv2.imwrite(string_argument, returned_frame)
                    print(f"[INFO] Image saved to {string_argument}")
                    self.log_ACTIVITY_HI_ImagingEnd()
                    self.downlinkImage_out(0, string_argument, Path(string_argument).name, 0, 0)
                # Capture errors
                except Exception as exc:
                    print(f"[WARNING] File write error: {exc}")
                    self.log_WARNING_HI_FileWriteError(string_argument, str(exc))
                    return_status = fprime_py.Fw.CmdResponse.T.EXECUTION_ERROR
            else:
                print("[WARNING] Imaging error occurred.")
                self.log_WARNING_HI_ImagingError()
                return_status = fprime_py.Fw.CmdResponse.T.EXECUTION_ERROR
        print(f"[DEBUG] TAKE_IMAGE command completed with status: {return_status}")
        self.cmdResponse_out(opCode, cmdSeq, fprime_py.Fw.CmdResponse(return_status))