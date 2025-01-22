# Quantum Random Number Generator (QRNG)

This project implements a Quantum Random Number Generator (QRNG) using IBM Qiskit based on [my medium post](https://medium.com/@marcell.ujlaki/exploring-quantum-computing-basic-quantum-random-number-generators-qrng-6637e5b36d36). It generates random numbers by leveraging quantum superposition and measurement.

## Features

- Uses IBM Quantum backend or Qiskit's AerSimulator.
- The simulator was developed with a T1/T2 thermal relaxation noise model to closely mimic real quantum devices.
- Optional enhancements:
  - Select the specified nth result from the list of measured values.
  - XOR operation with a user-defined value.

## Prerequisites

- Python 3.11+
- IBM Quantum account (optional)


## Installation Instructions

1. **Install Dependencies:**

   Open your terminal and execute:
   
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up IBM Quantum Account:**
   
   - Visit [IBM Quantum](https://quantum.ibm.com/) to create an account.
   - Retrieve your API token from the dashboard.
   - Save the token in your terminal using:
      ```bash
      python -c "from qiskit import IBMQ; IBMQ.save_account('<YOUR_API_TOKEN>')"
      ```

## Usage

1. Run the script:

   ```bash
   python qrng.py
   ```

2. Follow the prompts:

   - Specify the bit length (should be greater than 1, e.g., 32 or 64).
   - Optionally provide a value for shot selection.
   - Optionally provide a value for XOR operation.
   - Choose whether to use IBM Quantum or AerSimulator.

3. The generated quantum random number will be displayed.


### Example Output: 

<details>
   <summary>Using IBM service</summary>

```
Welcome to the Quantum Random Number Generator (QRNG)
Please ensure you have Qiskit and Qiskit IBM Runtime installed.

Enter the bit length for the random number (should be greater than 1, e.g., 32 or 64):
 64

Enhancements available:
 1. Use n-th result from the counts list.
 2. XOR with a custom value.
 3. None (default).

Choose an enhancement (1, 2, or 3): 3
 Selected enhancement: None

Force to use simulator instead of QPU?:
 0: No
 1: Yes

Answer: 0

-- Attempting to use IBM Qiskit Runtime -- 
 Connectiong to the account... 
  Connected.
   Account Information:
    Channel: ibm_quantum
    URL: https://auth.quantum-computing.ibm.com/api
    Instance: ibm-q/open/main
    Verify: True
    Private Endpoint: False

   Usage Information:
    Period Start: 2025-01-01T00:00:00.000Z
    Period End: 2025-01-31T23:59:59.999Z
    Instance: ibm-q/open/main
     Quota: 600
     Usage: 41
     Pending Jobs: 0
     Max Pending Jobs: 3

 Selecting backend...
  Connected to the backend:
   Name: ibm_brisbane
   Version: 1.1.66
   Number of Qubits: 127
   Local: False
   Simulator: False
   Conditional: False
   Open Pulse: True
   Memory: True
   Max Shots: 100000
   Dynamic Reprate Enabled: True
   Rep Delay Range: [0.0, 0.0005]
   Default Rep Delay: 0.00025
   Measurement Levels: [1, 2]
   Drive Channel Timestep (dt): 5e-10 ns
   Measurement Channel Timestep (dtm): 5e-10 ns
   Rep Times: [0.001]
   Measurement Kernels: ['hw_qmfk']
   Acquisition Latency: []
   Conditional Latency: []
   Max Circuits: 300
   Sample Name: family: Eagle, revision: 3
   Number of Registers: 1
   Credits Required: True
   Online Date: 2023-01-23 05:00:00+00:00
   Description: None
   Version: 2
   Parametric Pulses: ['gaussian', 'gaussian_square', 'gaussian_square_drag', 'drag', 'constant']
   Processor Type: {'family': 'Eagle', 'revision': 3}

 Creating job...
  Successfully created. Sampler job ID: [jobID]

  The result of the submitted job had 1 PUB(s) and has a value:
  PrimitiveResult([SamplerPubResult(data=DataBin(meas=BitArray(<shape=(), num_shots=4096, num_bits=64>)), metadata={'circuit_metadata': {}})], metadata={'execution': {'execution_spans': ExecutionSpans([SliceSpan(<start='starttime9', stop='endtime', size=4096>)])}, 'version': 2})

  The associated PubResult of this Sampler job has the following DataBins:
  DataBin(meas=BitArray(<shape=(), num_shots=4096, num_bits=64>))

  It has a key-value pair dict:
  dict_items([('meas', BitArray(<shape=(), num_shots=4096, num_bits=64>))])

  The metadata of the PrimitiveResult is:
   'execution' : {'execution_spans': ExecutionSpans([SliceSpan(<start='starttime9', stop='endtime', size=4096>)])},
   'version' : 2,

  The metadata of the PubResult result is:
   'circuit_metadata' : {},

--- Quantum RNG Results ---
Binary:       0001110010010110010111101110111000101101010101101111110111111111
Decimal:      2059938256624483839
Hexadecimal:  1c965eee2d56fdff
Octal:        162262756705525576777
Quantim Circuit used: 
```
![Quantim Circuit used](original-circuit.png "Quantim Circuit used")

</details>

<details>
  <summary>Using simulator</summary>

```plaintext
Welcome to the Quantum Random Number Generator (QRNG)
Please ensure you have Qiskit and Qiskit IBM Runtime installed.

Enter the bit length for the random number (should be greater than 1, e.g., 32 or 64):
 7

Enhancements available:
 1. Use n-th result from the counts list.
 2. XOR with a custom value.
 3. None (default).

Choose an enhancement (1, 2, or 3): 1

 Enter a valid positive integer for the n-th result. Possible outcomes: 128: 14
 Selected enhancement: nth_count

Force to use simulator instead of QPU?:
 0: No
 1: Yes

Answer: 1

-- Enforcing AerSimulator usage -- 
AerSimulator Configuration Details:
  Controller: <qiskit_aer.backends.controller_wrappers.aer_controller_execute object at 0xffff711c3d30>
  Simulator Name: aer_simulator
  Simulator Description: A C++ Qasm simulator with noise
  Backend Version: 0.15.1
  shots: 1024
  method: automatic
  device: CPU
  precision: double
  max_parallel_threads: 4
  max_parallel_shots: 8
  fusion_enable: True
  fusion_verbose: False
  noise_model: NoiseModel:
  Basis gates: ['cx', 'id', 'rz', 'sx', 'u2', 'u3']
  Instructions with noise: ['u2', 'u3', 'measure', 'cx', 'reset']
  Qubits with noise: [0, 1, 2, 3, 4, 5, 6]
  Specific qubit errors: [('reset', (0,)), ('reset', (1,)), ('reset', (2,)), ('reset', (3,)), ('reset', (4,)), ('reset', (5,)), ('reset', (6,)), ('measure', (0,)), ('measure', (1,)), ('measure', (2,)), ('measure', (3,)), ('measure', (4,)), ('measure', (5,)), ('measure', (6,)), ('u2', (0,)), ('u2', (1,)), ('u2', (2,)), ('u2', (3,)), ('u2', (4,)), ('u2', (5,)), ('u2', (6,)), ('u3', (0,)), ('u3', (1,)), ('u3', (2,)), ('u3', (3,)), ('u3', (4,)), ('u3', (5,)), ('u3', (6,)), ('cx', (0, 0)), ('cx', (0, 1)), ('cx', (0, 2)), ('cx', (0, 3)), ('cx', (0, 4)), ('cx', (0, 5)), ('cx', (0, 6)), ('cx', (1, 0)), ('cx', (1, 1)), ('cx', (1, 2)), ('cx', (1, 3)), ('cx', (1, 4)), ('cx', (1, 5)), ('cx', (1, 6)), ('cx', (2, 0)), ('cx', (2, 1)), ('cx', (2, 2)), ('cx', (2, 3)), ('cx', (2, 4)), ('cx', (2, 5)), ('cx', (2, 6)), ('cx', (3, 0)), ('cx', (3, 1)), ('cx', (3, 2)), ('cx', (3, 3)), ('cx', (3, 4)), ('cx', (3, 5)), ('cx', (3, 6)), ('cx', (4, 0)), ('cx', (4, 1)), ('cx', (4, 2)), ('cx', (4, 3)), ('cx', (4, 4)), ('cx', (4, 5)), ('cx', (4, 6)), ('cx', (5, 0)), ('cx', (5, 1)), ('cx', (5, 2)), ('cx', (5, 3)), ('cx', (5, 4)), ('cx', (5, 5)), ('cx', (5, 6)), ('cx', (6, 0)), ('cx', (6, 1)), ('cx', (6, 2)), ('cx', (6, 3)), ('cx', (6, 4)), ('cx', (6, 5)), ('cx', (6, 6))]
  batched_shots_gpu_max_qubits: 16
  num_threads_per_device: 1
  tensor_network_num_sampling_qubits: 10

--- Quantum RNG Results ---
Binary:       0000100
Decimal:      4
Hexadecimal:  4
Octal:        4
Quantim Circuit used: 

        ┌─────────┐ ░ ┌─┐                  
   q_0: ┤ U2(0,π) ├─░─┤M├──────────────────
        ├─────────┤ ░ └╥┘┌─┐               
   q_1: ┤ U2(0,π) ├─░──╫─┤M├───────────────
        ├─────────┤ ░  ║ └╥┘┌─┐            
   q_2: ┤ U2(0,π) ├─░──╫──╫─┤M├────────────
        ├─────────┤ ░  ║  ║ └╥┘┌─┐         
   q_3: ┤ U2(0,π) ├─░──╫──╫──╫─┤M├─────────
        ├─────────┤ ░  ║  ║  ║ └╥┘┌─┐      
   q_4: ┤ U2(0,π) ├─░──╫──╫──╫──╫─┤M├──────
        ├─────────┤ ░  ║  ║  ║  ║ └╥┘┌─┐   
   q_5: ┤ U2(0,π) ├─░──╫──╫──╫──╫──╫─┤M├───
        ├─────────┤ ░  ║  ║  ║  ║  ║ └╥┘┌─┐
   q_6: ┤ U2(0,π) ├─░──╫──╫──╫──╫──╫──╫─┤M├
        └─────────┘ ░  ║  ║  ║  ║  ║  ║ └╥┘
meas: 7/═══════════════╩══╩══╩══╩══╩══╩══╩═
                       0  1  2  3  4  5  6 
```

</details>

## Error Handling

- **Timeouts:** If IBM Quantum backend is unresponsive for 25 minutes, the script will fall back to AerSimulator.
- **Memory Constraints:** The script avoids exceeding hardware limitations by dynamically adjusting the backend.

## Contributions

Contributions are welcome! If you have any suggestions or improvements, feel free to fork this repository and/or submit a pull request. For questions or feedback, reach out on GitHub: [@marcell-ujlaki](https://github.com/marcell-ujlaki).

## References

- [Exploring Quantum Computing: Basic Quantum Random Number Generators (QRNG)](https://medium.com/@marcell.ujlaki/exploring-quantum-computing-basic-quantum-random-number-generators-qrng-6637e5b36d36)
- [Qiskit Documentation](https://qiskit.org/documentation/)