# Quantum Fourier Transform (QFT) Implementation

This Python code demonstrates the implementation of the Quantum Fourier Transform (QFT) using Qiskit, a Python library for quantum computing.

## Requirements

- Python 3.x
- Qiskit
- NumPy
- Matplotlib
- pylatexenc

Ensure you have these libraries installed before running the code. If not, you can install them using pip:

```bash
pip install qiskit qiskit-aer numpy matplotlib pylatexenc
```

or

```bash
python -m venv QFT
source QFT/bin/activate
pip install -r requirements.txt
```

## Code Overview

The provided code implements the Quantum Fourier Transform using the following main functions:

- `qft_rotations(circuit, n)`: Applies Hadamard gates and controlled phase gates to perform rotations required for the QFT.
- `swap_registers(circuit, n)`: Swaps qubits to finalize the QFT operation.
- `qft(circuit, n)`: Combines rotations and register swaps to execute the Quantum Fourier Transform.

Additionally, the code contains a function `qc_init(number)` to initialize a quantum circuit with a specified integer number.

## Usage

1. Script will ask for your input. Give the `number` variable to the desired integer value.
2. Run the code in a `Python` environment.
3. The code will generate a quantum circuit representing the `QFT` and save it as `quantum_circuit.png`.s
4. It will also perform a simulation of the `QFT` using the `Aer simulator` from `Qiskit`, visualizing the statevector using Bloch sphere representation and LaTeX-formatted statevector information.

Feel free to experiment and explore the code to understand the Quantum Fourier Transform and its applications in quantum computing.
