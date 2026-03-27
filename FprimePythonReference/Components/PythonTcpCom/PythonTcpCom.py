""" PythonTcpCom Python component implementation

This is the Python implementation for the PythonTcpCom component. This class extends the auto-coded python base
class PythonTcpComBase that provides the necessary plumbing to connect to the C++ stub connected to the rest of
the F Prime topology.
"""
import socket
import threading
import fprime_py
from PythonTcpComBaseAc import PythonTcpComBase


class PythonTcpCom(PythonTcpComBase):
    """ Python implementation for the PythonTcpCom component """
    def __init__(self):
        """ Construct the component
        
        The component is constructed during the "init" phase when the component is originally called. During this phase
        the F Prime topology is not yet fully constructed, so only basic initialization should be done here.
        """
        super().__init__()
        self.configure("localhost", 50000)
        self.start()
    
    def configure(self, host, port):
        """ Start the TCP communication process
        
        This method is called during the configure phase of the component setup. This setup will establish and bind the
        TCP socket connection used for communication.

        Args:
            host: The host IP address or name to bind to
            port: The port number to bind to
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind and begin listening
        self.server.bind((host, port))
        self.server.listen()
        self.done_receiving = False

    def start(self):
        """ Start the TCP communication process
        
        This method is called during the start phase of the component setup. This setup will start listening for incoming
        TCP connections and spawn a new thread to handle each connection.
        """
        self.thread = threading.Thread(target=self.receive_thread, args=())
        self.thread.start()

    def stop(self):
        """ Stop the TCP communication process
        
        This method is called during the stop phase of the component teardown. This setup will close the TCP connection
        and stop the receive thread.
        """
        self.done_receiving = True
        if self.client_socket:
            self.client_socket.close()
        self.server.close()
        self.thread.join()

    def receive_thread(self):
        """ Thread that receives data from the TCP connection """
        self.client_socket, address = self.server.accept()
        print(f"[INFO] Accepted connection from: {address}")
        self.comStatusOut_out(0, fprime_py.Fw.Success(fprime_py.Fw.Success.T.SUCCESS))
        while not self.done_receiving:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    continue
                self.dataOut_out(0, fprime_py.Fw.Buffer(data), fprime_py.ComCfg.FrameContext())
            except Exception as exc:
                print(f"[ERROR] Error in receive_thread: {exc}")

    def dataIn_handler(self, portNum, data, context):
        """ Handle the dataIn port """
        try:
            #assert self.client_socket is not None, "client_socket must be set before dataIn_handler is called"
            self.client_socket.sendall(data.getData())
            self.dataReturnOut_out(portNum, data, context)
            self.comStatusOut_out(0, fprime_py.Fw.Success(fprime_py.Fw.Success.T.SUCCESS))
        except Exception as exc:
            print(f"[ERROR] Error in dataIn_handler: {exc}")
            #self.comStatusOut_out(0, fprime_py.Fw.Success(fprime_py.Fw.Success.T.FAILURE))

    def dataReturnIn_handler(self, portNum, data, context):
        """ Handle the dataReturnIn port """
        pass # Python is garbage collected