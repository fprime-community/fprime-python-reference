module FprimePythonReference {
    @ An active component implemented in Python
    @ fprime-python
    active component ActiveImager {
        @ Take image command. This will take an image with the default camera and send the image for downlink via the
        @ file downlink service.
        async command TAKE_IMAGE(string_argument: string) drop

        @ Event fired when imaging starts
        event ImagingStart severity activity high \
            format "Imaging started"

        @ Event fired when imaging completes successfully
        event ImagingEnd severity activity high \
            format "Imaging completed successfully"

        @ Event fired when an imaging error occurs
        event ImagingError() severity warning high \
            format "Image capture failed"

        @ Event fired when camera is not available
        event CameraUnavailable severity warning high \
            format "Camera is not available"

        @ Event fired when file write fails
        event FileWriteError(filename: string, error: string) severity warning high \
            format "Failed to write image file: {} with error: {}"
        
        @ Send files to the ground via the FileDownlink service
        output port downlinkImage: Svc.SendFileRequest

        @ Send files to the ground via the FileDownlink service
        async input port takeImage: FprimePythonReference.Image

        ###############################################################################
        # Standard AC Ports: Required for Channels, Events, Commands, and Parameters  #
        ###############################################################################
        @ Port for requesting the current time
        time get port timeCaller

        @ Port for sending command registrations
        command reg port cmdRegOut

        @ Port for receiving commands
        command recv port cmdIn

        @ Port for sending command responses
        command resp port cmdResponseOut

        @ Port for sending textual representation of events
        text event port logTextOut

        @ Port for sending events to downlink
        event port logOut

        @ Port for sending telemetry channels to downlink
        telemetry port tlmOut

        @ Port to return the value of a parameter
        param get port prmGetOut

        @Port to set the value of a parameter
        param set port prmSetOut

    }
}
