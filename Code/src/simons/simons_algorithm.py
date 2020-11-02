import itertools
import random
import time

from qiskit import (Aer, ClassicalRegister,
                    QuantumCircuit, QuantumRegister,
                    execute)
from qiskit.visualization import plot_histogram

from simons_oracle import simons_oracle

random.seed(time.monotonic())

# Get backend
backend = Aer.get_backend('qasm_simulator')

# Length of input
n = 4

# Initialise input and output registers
input = QuantumRegister(n, "input")
output = QuantumRegister(n, "output")
result = ClassicalRegister(n)

# Initialise circuit
circuit = QuantumCircuit(input, output, result)

# Generate random secret string
secret_input = [0 for i in range(n)]
while secret_input.count(0) == n:
    secret_input = [random.choice([0, 1]) for i in range(n)]
print(f"Secret string - {''.join([str(bit) for bit in secret_input])}")

# Test Oracle
for seq in itertools.product(["0", "1"], repeat=n):
    # Copy circuit
    circ = circuit.copy()

    # Inititialise input qubits
    desired_vector = [0 for i in range(2**n)]
    desired_vector[int("".join(seq), 2)] = 1
    circ.initialize(desired_vector, input)

    # Apply simons oracle circuit
    simons_oracle(circ, input, output, secret_input)

    # Perform measurement
    circ.measure(output, result)
    print(f"{seq} - {execute(circ, backend).result().get_counts(circ)}")
