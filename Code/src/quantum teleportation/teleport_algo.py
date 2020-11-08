import numpy as np
from qiskit import *
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.extensions import Initialize
from qiskit_textbook.tools import random_state, array_to_latex
from matplotlib import *


def teleport_gate():
    inp = QuantumRegister(1)
    inter = QuantumRegister(1)
    out = QuantumRegister(1)
    circuit = QuantumCircuit(inp, inter, out)
    circuit.h(inter)
    circuit.cx(inter, out)
    circuit.cx(inp, inter)
    circuit.h(inp)
    return circuit.to_gate(label="Entangle for teleport")


def quantum_teleport(qc, input_reg, output_reg, intermediate_reg=None):
    # Add the needed registers
    crz = ClassicalRegister(1, name='crz')
    crx = ClassicalRegister(1, name='crx')
    if intermediate_reg is None:
        intermediate_reg = QuantumRegister(1, name='intermediate register')
        qc.add_register(intermediate_reg)
    qc.add_register(crz)
    qc.add_register(crx)

    # Proceed to teleportation.
    qc.append(teleport_gate(), [input_reg, intermediate_reg, output_reg])
    qc.barrier()
    qc.measure(input_reg, crz)
    qc.measure(intermediate_reg, crx)
    qc.barrier()
    qc.x(output_reg).c_if(crx, 1)
    qc.z(output_reg).c_if(crz, 1)
