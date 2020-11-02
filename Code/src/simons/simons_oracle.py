from typing import List

from qiskit import QuantumCircuit, QuantumRegister


def simons_oracle(circuit: QuantumCircuit,
                  input: QuantumRegister,
                  output: QuantumRegister,
                  secret_input: List[int]) -> QuantumRegister:
    # Size of secret, input and output
    (s, n) = (input.size, input.size)
    # Register holding the secret string
    secret = QuantumRegister(s, "secret")
    circuit.add_register(secret)

    # Encode it in the quantum register
    for i in range(s):
        if secret_input[i]:
            circuit.x(secret[i])

    circuit.barrier()

    # Copy input register to output register
    for i in range(n):
        circuit.cx(input[i], output[i])

    circuit.barrier()

    # Find msb of secret string
    msb = secret_input.index(1)

    # Create 2-1 mapping
    for i in range(n):
        circuit.cx(input[msb], output[i])

    circuit.barrier()

    # Randomly flip qubits for further obfuscation
    for i in range(n):
        if i % 3 == 0:
            circuit.x(output[i])

    circuit.barrier()

    return secret
