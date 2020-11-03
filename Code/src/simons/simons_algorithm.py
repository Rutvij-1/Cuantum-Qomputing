import itertools

from qiskit import (Aer, ClassicalRegister,
                    QuantumCircuit, QuantumRegister,
                    execute)
from qiskit.visualization import plot_histogram

from simons_oracle import simons_oracle


# Get backend
backend = Aer.get_backend('qasm_simulator')

# Length of input
n = 4

# Initialise input, output and secret registers
input = QuantumRegister(n, "input")
output = QuantumRegister(n, "output")
secret = QuantumRegister(n, "secret")
result = ClassicalRegister(n)

(oracle, secret_input) = simons_oracle(n)
print(f"Secret string - {''.join([str(bit) for bit in secret_input])}")

# Test Oracle
for seq in itertools.product(["0", "1"], repeat=n):
    # Initialize circuit
    circuit = QuantumCircuit(input, output, secret, result)

    # Inititialise input qubits
    desired_vector = [0 for i in range(2**n)]
    desired_vector[int("".join(seq), 2)] = 1
    circuit.initialize(desired_vector, input)

    circuit.append(oracle, [*input, *output, *secret])

    # Perform measurement
    circuit.measure(output, result)
    print(f"{seq} - {execute(circuit, backend).result().get_counts(circuit)}")
