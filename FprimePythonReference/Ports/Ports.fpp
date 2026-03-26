module FprimePythonReference {

@ Port to take an image
port Image(filename: string)

@ Sample port for arguments
port PythonPort(arg1: PythonEnumeration, arg2: PythonComplexStruct)

@ Sample port for return value
port PythonReturnPort() -> PythonEnumeration


}