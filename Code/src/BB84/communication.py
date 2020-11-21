import bitarray
import numpy as np
import subprocess as sp
from qubit_interaction import to_qubits, to_cbits
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector

def compare_bases(bases1, bases2, bits):
    formed_key = []
    for i in range(len(bases1)):
        if bases1[i] == bases2[i]:
            formed_key.append(bits[i])
    
    return formed_key

def run_simul(is_eve):
    tmp = sp.call('clear', shell=True)
    
    if is_eve:
        print("You know that Eve is listening, but Alice and Bob don't know this.\n")
    else:
        print("You know that Eve is not listening, but Alice and Bob don't know this.\n")

    print("To check if Eve is listening, Alice is going to send a message to Bob over the quantum channel.")

    alice_message = input("Choose a message for Alice to send (between 20 and 100 characters): ") or "Need a smol message smh"
    tmp = sp.call('clear', shell=True)

    if(len(alice_message)>100 or len(alice_message)<20):
        alice_message = "Smh the code will just use this string instead"

    alice_bits = bitarray.bitarray()
    alice_bits.frombytes(alice_message.encode('utf-8'))
    alice_bits = np.array(list(alice_bits)).astype(int)

    print("Alice is going to send this message:\n", alice_bits)

    input("\nPress any key to continue...")
    tmp = sp.call('clear', shell=True)

    print("Alice chooses to encode the bits on the standard basis(Z) or the signed basis(X) at random and sends the encoded message to Bob.")

    np.random.seed(seed=0)
    alice_bases = np.random.randint(2, size=(len(alice_bits)))

    encoded_message = to_qubits(alice_bits, alice_bases)

    input("\nPress any key to continue...")
    tmp = sp.call('clear', shell=True)

    if is_eve:
        print("Oops! Eve has intercepted the encoded message and measured the qubits. Alice and Bob don't know yet that this happened. Eve sends the qubits she received to Bob.")
        
        eve_bases = np.random.randint(2, size=(len(alice_bits)))
        eve_bits = to_cbits(encoded_message, eve_bases)
        eve_bits = np.array(eve_bits)
        
        input("\nPress any key to continue...")
        tmp = sp.call('clear', shell=True)

    print("Bob chooses to measure the bits he received on the standard basis(Z) or the signed basis(X) at random.")
    input("\nPress any key to continue...")
    tmp = sp.call('clear', shell=True)

    bob_bases = np.random.randint(2, size=(len(alice_bits)))

    print("Bob measures the qubits using the bases he chose and obtains this message:")
    bob_bits = to_cbits(encoded_message, bob_bases)
    bob_bits = np.array(bob_bits)
    print(bob_bits)

    input("\nPress any key to continue...")
    tmp = sp.call('clear', shell=True)

    print("Alice and Bob send the bases they used to each other. If they chose the same base to encode and decode a bit, they keep that bit. They drop that bit if they used different bases to encode and decode it.")

    alice_key = compare_bases(alice_bases, bob_bases, alice_bits)
    alice_key = np.array(alice_key)
    bob_key = compare_bases(alice_bases, bob_bases, bob_bits)
    bob_key = np.array(bob_key)

    input("\nPress any key to continue...")
    tmp = sp.call('clear', shell=True)

    print("Alice and Bob now choose a small part of the bits they end up with and send it to each other.")

    sample_size = int(len(alice_key)/3)

    alice_sample = alice_key[-sample_size:]
    bob_sample = bob_key[-sample_size:]

    print("Alice sent:".ljust(12), alice_sample)
    print("Bob sent:".ljust(12), bob_sample)

    input("\nPress any key to continue...")
    tmp = sp.call('clear', shell=True)

    if np.array_equal(alice_sample, bob_sample):
        print("Alice and Bob believe that Eve has not intercepted their key, and their communication channel is secure.")
        if is_eve:
            print("However, they are wrong! Eve has intercepted their message. You knew all along didn't you?")
        else:
            print("They are right! Eve has not intercepted their message. You knew all along didn't you?")

    else:
        print("Alice and Bob believe that Eve has intercepted their key, and their communication channel is not secure.")
        if is_eve:
            print("They are right! Eve has intercepted their message. You knew all along didn't you?")
        else:
            print("However, they are wrong! Eve has not intercepted their message. You knew all along didn't you?")
    return