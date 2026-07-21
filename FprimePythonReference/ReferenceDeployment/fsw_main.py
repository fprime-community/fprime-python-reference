""" fsw_main.py:

Main file to launch F Prime from the python interpreter. This will set up the topology state, start rate groups, and
run the F Prime system.

Supplies required entrypoint: fsw_main() for use with fprime-python-runner.
"""
import fprime_py
import argparse
import signal

def parse_args():
    """ Parse command line arguments for F Prime execution """
    parser = argparse.ArgumentParser(description="F Prime Python Main Flight Software Entry Point")
    parser.add_argument(
        "--hostname",
        type=str,
        default="127.0.0.1",
        help="Hostname allowing the F Prime topology to connect via TcpClient to the fprime-gds"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=50000,
        help="Port for the F Prime topology to connect via TcpClient to the fprime-gds"
    )
    return parser.parse_args()


def handle_sigterm(signum, frame):
    """ Shut down gracefully on SIGTERM, mirroring CTRL-C handling """
    raise KeyboardInterrupt


def fsw_main():
    """ Main entrypoint for F Prime system
    
    This function sets up the topology, starts rate groups, and tears down the topology after execution.
    fprime-python-runner requires this entrypoint to be called "fsw_main" and have no arguments.
    """
    # Set up topology state from command line arguments
    args = parse_args()
    signal.signal(signal.SIGTERM, handle_sigterm)
    topology_state = fprime_py.TopologyState()
    topology_state.hostname = args.hostname
    topology_state.port = args.port
    fprime_py.Os.init()

    # Launch F Prime system
    try:
        print("[INFO] Launching F Prime ")
        fprime_py.ReferenceDeployment.setup(topology_state)
        fprime_py.ReferenceDeployment.Instances.pythonCom.configure(topology_state.hostname, topology_state.port)
        fprime_py.ReferenceDeployment.Instances.pythonCom.start()
        fprime_py.ReferenceDeployment.Instances.timer.driveRateGroup(fprime_py.Fw.TimeInterval(1, 0))
        fprime_py.ReferenceDeployment.Instances.pythonCom.stop()
    except KeyboardInterrupt:
        print("[INFO] CTRL-C received, shutting down F Prime")
    except Exception as e:
        print(f"[ERROR] Failed to start F Prime: {e}")
    fprime_py.ReferenceDeployment.teardown(topology_state)
    print("[INFO] F Prime shutdown complete")


# For cases when run without fprime-python-runner
if __name__ == "__main__":
    fsw_main()
