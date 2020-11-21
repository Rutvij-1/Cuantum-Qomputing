import numpy as np
from qiskit import *
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.extensions import Initialize
from qiskit_textbook.tools import random_state, array_to_latex
from matplotlib import *
import teleport_algo


# Initialise backend.
backend = Aer.get_backend('statevector_simulator')

# Initialise Circuit.
inp = QuantumRegister(1, name='input register')
out = QuantumRegister(1, name='output register')
circuit = QuantumCircuit(inp, out)

# Set input register to a random state.
psi = random_state(1)
array_to_latex(psi, pretext="|\\psi\\rangle =")
plot_bloch_multivector(psi)
init_gate = Initialize(psi)
circuit.append(init_gate, [inp])
circuit.barrier()

# Perform teleportation.
teleport_algo.quantum_teleport(circuit, inp, out)

# Execute simulation and display result.
job = execute(circuit, backend)
result = job.result()
outputstate = result.get_statevector(circuit, decimals=4)
array_to_latex(psi, pretext="|output\\rangle =")
plot_bloch_multivector(outputstate)

circuit.draw()

pyplot.show()
