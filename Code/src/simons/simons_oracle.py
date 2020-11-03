import random
import time
from typing import List, Tuple

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Gate

random.seed(time.monotonic())


def simons_oracle(size: int) -> Tuple[Gate, List[int]]:
    # Register holding the secret string
    secret = QuantumRegister(size, "secret")

    # Input and Output registers
    input = QuantumRegister(size, "input")
    output = QuantumRegister(size, "output")

    # Initialize circuit
    oracle = QuantumCircuit(input, output, secret)

    # Generate random secret string
    secret_input = [0 for i in range(size)]
    while secret_input.count(0) == size:
        secret_input = [random.choice([0, 1]) for i in range(size)]

    # Encode it in the quantum register
    for i in range(size):
        if secret_input[i]:
            oracle.x(secret[i])

    # Copy input register to output register
    for i in range(size):
        oracle.cx(input[i], output[i])

    # Find msb of secret string
    msb = secret_input.index(1)

    # Create 2-1 mapping
    for i in range(size):
        oracle.ccx(input[msb], secret[i], output[i])

    # Randomly flip qubits for further obfuscation
    for i in range(size):
        if i % 3 == 0:
            oracle.x(output[i])

    return oracle.to_gate(label="oracle"), secret_input
