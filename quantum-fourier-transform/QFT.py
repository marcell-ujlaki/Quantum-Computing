import numpy as np
from numpy import pi
from qiskit import QuantumCircuit, Aer, IBMQ
from qiskit.visualization import plot_bloch_multivector
from qiskit.visualization import circuit_drawer

def qft_rotations(circuit, n):
    if n == 0:
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(pi/2**(n-qubit), qubit, n) # CROT from qubit n to the actual qubit
    qft_rotations(circuit, n)

def swap_registers(circuit, n):
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit

def qft(circuit, n):
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

def qc_init(number):
    binary = bin(number)[2:]
    qubits = len(binary)

    qc = QuantumCircuit(qubits)

    # Apply X gate to qubits based on binary representation
    for index, bit in enumerate(reversed(binary)):
        if bit == '1':
            qc.x(index)
    return qc, qubits

# Ask for number input
while True:
    try:
        number = int(input("Please enter a number: "))
        break  # Break the loop if the input is a valid number
    except ValueError:
        print("That's not a valid number. Please try again.")

print("You entered:", number)

qc, qubits = qc_init(number)
qft(qc,qubits)
#display(qc.draw('mpl',style="iqp"))

# Save the output
quantum_circuit = circuit_drawer(qc, output='mpl',style="iqp")
quantum_circuit.savefig('quantum_circuit.png')

# Start the simulation

sim = Aer.get_backend("aer_simulator")
qc_init = qc.copy()
qc_init.save_statevector()
statevector = sim.run(qc_init).result().get_statevector()
print(statevector)