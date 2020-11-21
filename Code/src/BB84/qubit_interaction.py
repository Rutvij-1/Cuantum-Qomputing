from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector

def to_qubits(bits, bases):
    encoded_message = []
    for i in range(len(bits)):
        qc = QuantumCircuit(1,1)
        if bases[i] == 0:
            if bits[i] == 0:
                qc.i(0)
            else:
                qc.x(0)
        else:
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        qc.barrier()
        encoded_message.append(qc)
    return encoded_message

def to_cbits(qubits, bases):
    backend = Aer.get_backend('qasm_simulator')
    decoded_message = []
    for i in range(len(qubits)):
        if bases[i] == 0:
            qubits[i].measure(0,0)
        if bases[i] == 1:
            qubits[i].h(0)
            qubits[i].measure(0,0)
        result = execute(qubits[i], backend, shots=1, memory=True).result()
        measured_bit = int(result.get_memory()[0])
        decoded_message.append(measured_bit)
    return decoded_message