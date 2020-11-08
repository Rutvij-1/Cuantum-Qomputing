import numpy as np
from qiskit import *
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.extensions import Initialize
from qiskit_textbook.tools import random_state, array_to_latex
from matplotlib import *


def quantum_teleport(qc, input_reg, output_reg):
    # Add the needed registers
    crz = ClassicalRegister(1, name='crz')
    crx = ClassicalRegister(1, name='crx')
    intermediate_reg = QuantumRegister(1, name='intermediate register')
    qc.add_register(intermediate_reg)
    qc.add_register(crz)
    qc.add_register(crx)

    # Proceed to teleportation.
    qc.h(intermediate_reg)
    qc.cx(intermediate_reg, output_reg)
    qc.barrier()
    qc.cx(input_reg, intermediate_reg)
    qc.h(input_reg)
    qc.barrier()
    qc.measure(input_reg, crz)
    qc.measure(intermediate_reg, crx)
    qc.barrier()
    qc.x(output_reg).c_if(crx, 1)
    qc.z(output_reg).c_if(crz, 1)
