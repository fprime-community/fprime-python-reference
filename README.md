# Fprime Python Reference: Implementing Component in Python

`fprime-python` provides an autocoder for automatically binding F Prime C++ code to Python. It is designed to work within the Python interpreter allowing access to standard F Prime components and topologies.

`fprime-python-reference` (this repository) provides a reference project that builds on top of `fprime-python`.

## Example Components

The `fprime-python-reference` repository includes example components that demonstrate how to implement F Prime components in Python. These components are located in the `FprimePythonReference/Components` directory and include:

1. ActiveImager: An `active` component that uses Python and OpenCV to capture/downlink camera images
2. PythonGc: A `queued` component that demonstrates how to telemeter Garbage Collection information
3. PythonTcpCom: A `passive` component that implements a communication interface using TCP sockets

> [!CAUTION]
> This reference will use your system's camera.

> [!NOTE]
> The `fprime-python` rate group driver is also used in this reference.

## Building

First, clone the project using `fprime-bootstrap`, which will ensure that `requirements.txt` is properly installed:

```bash
pip install -U fprime-bootstrap
fprime-bootstrap clone https://github.com/fprime-community/fprime-python-reference.git
```

Next, source the environment created by `fprime-bootstrap` and build/run as usual:

```bash
. fprime-venv/bin/activate
fprime-util generate
fprime-util build
```

> [!CAUTION]
> The build for `fprime-python` projects will be much slower as it is autocoding more items, as well as running complete model exporting with `fpp-to-json`.

## Running

To run the project, first run the GDS in the root of the project:

```bash
. fprime-venv/bin/activate
fprime-gds
```

> [!NOTE]
> This automatically starts the GDS without running the executable.

Next, run Python with the bindings installed:

```bash
python3 build-artifacts/python/fsw_main.py
```

