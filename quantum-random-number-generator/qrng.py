import random
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2 as Sampler
from qiskit_ibm_runtime.ibm_backend import IBMBackend
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


def validate_positive_integer(input_str: str = '') -> int:
    """Validates user input as a positive integer."""
    try:
        value = int(input_str)
        if value <= 0:
            raise ValueError
        return value

    except ValueError:
        return None

def use_ibm_runtime(
        backend: IBMBackend = None,
        qc: QuantumCircuit = None,
        threshold: int = 4096) -> tuple[QuantumCircuit, dict]:
    try:

        pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
        isa_circuit = pm.run(qc)

        with Session(backend=backend, max_time="25m") as session:
            sampler = Sampler(mode=session)
            print(" Creating job...")
            job = sampler.run([isa_circuit], shots=threshold)
            print(f"  Successfully created. Sampler job ID: {job.job_id()}\n")
            job_result = job.result()
            session.close()

        num_pubs = len(job_result)
        pub_result = job_result[0]
        data_bins = pub_result.data
        key_value_pairs = data_bins.items()
        bitstring_counts = data_bins.meas.get_counts()
        primitive_metadata = job_result.metadata
        pub_metadata = pub_result.metadata

        print(
            f"  The result of the submitted job had {num_pubs} PUB(s) and has a value:\n  {job_result}\n"
        )
        print(
            f"  The associated PubResult of this Sampler job has the following DataBins:\n  {data_bins}\n"
        )
        print(f"  It has a key-value pair dict:\n  {key_value_pairs}\n")

        print("  The metadata of the PrimitiveResult is:")
        for key, val in primitive_metadata.items():
            print(f"   '{key}' : {val},")

        print("\n  The metadata of the PubResult result is:")
        for key, val in pub_metadata.items():
            print(f"   '{key}' : {val},")

        return isa_circuit, bitstring_counts

    except Exception as e:
        print(f" Error during execution on IBM Quantum Runtime: {e}\n\n Switching to simulator")

def use_simulator(
        length: int = 0,
        qc: QuantumCircuit = None,
        threshold: int = 4096) -> tuple[QuantumCircuit, dict]:

    # Adding T1/T2 thermal relaxation noise model for closely mimicing real-world quantum devices
    noise_model = NoiseModel()

    T1s = np.random.normal(50e3, 10e3, length)
    T2s = np.random.normal(70e3, 10e3, length)
    T2s = np.array([min(T2s[j], 2 * T1s[j]) for j in range(length)])

    time_u1 = 0
    time_u2 = 50
    time_u3 = 100
    time_cx = 300
    time_reset = 1000
    time_measure = 1000

    errors_reset = [thermal_relaxation_error(t1, t2, time_reset)
                    for t1, t2 in zip(T1s, T2s)]
    errors_measure = [thermal_relaxation_error(t1, t2, time_measure)
                    for t1, t2 in zip(T1s, T2s)]
    errors_u1  = [thermal_relaxation_error(t1, t2, time_u1)
                for t1, t2 in zip(T1s, T2s)]
    errors_u2  = [thermal_relaxation_error(t1, t2, time_u2)
                for t1, t2 in zip(T1s, T2s)]
    errors_u3  = [thermal_relaxation_error(t1, t2, time_u3)
                for t1, t2 in zip(T1s, T2s)]
    errors_cx = [[thermal_relaxation_error(t1a, t2a, time_cx).expand(
                thermal_relaxation_error(t1b, t2b, time_cx))
                for t1a, t2a in zip(T1s, T2s)]
                for t1b, t2b in zip(T1s, T2s)]
            
    for j in range(length):
        noise_model.add_quantum_error(errors_reset[j], "reset", [j])
        noise_model.add_quantum_error(errors_measure[j], "measure", [j])
        noise_model.add_quantum_error(errors_u1[j], "u1", [j])
        noise_model.add_quantum_error(errors_u2[j], "u2", [j])
        noise_model.add_quantum_error(errors_u3[j], "u3", [j])
        for k in range(length):
            noise_model.add_quantum_error(errors_cx[j][k], "cx", [j, k])

    simulator = AerSimulator(
        method='automatic',
        noise_model=noise_model,
        precision='double',
        max_parallel_shots=8,
        max_parallel_threads=4,
        shot_branching_enable=True,
        device='CPU'
    )

    print("AerSimulator Configuration Details:")
    print(f"  Controller: {simulator._controller}")
    print(f"  Simulator Name: {simulator.name}")
    print(f"  Simulator Description: {simulator.description}")
    print(f"  Backend Version: {simulator.backend_version}")
    print(f"  shots: {simulator.options.shots}")
    print(f"  method: {simulator.options.method}")
    print(f"  device: {simulator.options.device}")
    print(f"  precision: {simulator.options.precision}")
    print(f"  max_parallel_threads: {simulator.options.max_parallel_threads}")
    print(f"  max_parallel_shots: {simulator.options.max_parallel_shots}")
    print(f"  fusion_enable: {simulator.options.fusion_enable}")
    print(f"  fusion_verbose: {simulator.options.fusion_verbose}")
    print(f"  noise_model: {simulator.options.noise_model}")
    print(f"  batched_shots_gpu_max_qubits: {simulator.options.batched_shots_gpu_max_qubits}")
    print(f"  num_threads_per_device: {simulator.options.num_threads_per_device}")
    print(f"  tensor_network_num_sampling_qubits: {simulator.options.tensor_network_num_sampling_qubits}")


    try:
        circ = transpile(qc, simulator)
        result = simulator.run(circ, shots=threshold, memory=True).result()
        counts = result.get_counts()

        return circ, counts

    except Exception as e:
        print(f" An error occurred during simulation: {e}")

def generate_qrng(
        bit_length: int = 2, 
        enhancement: int = 1,
        nth_count: int = 1, 
        xor_value: int = None,
        force_using_simulator: int = None) -> str:

    try:
        if force_using_simulator == 0:
            print("\n-- Attempting to use IBM Qiskit Runtime -- ")
            print(" Connectiong to the account... ")
            service = QiskitRuntimeService()
            account = service.active_account()
            usage = service.usage()

            print("  Connected.")
            print("   Account Information:")
            print(f"    Channel: {account['channel']}")
            print(f"    URL: {account['url']}")
            print(f"    Instance: {account['instance']}")
            print(f"    Verify: {account['verify']}")
            print(f"    Private Endpoint: {account['private_endpoint']}\n")

            print("   Usage Information:")
            print(f"    Period Start: {usage['period']['start']}")
            print(f"    Period End: {usage['period']['end']}")

            for instance_usage in usage['byInstance']:
                print(f"    Instance: {instance_usage['instance']}")
                print(f"     Quota: {instance_usage['quota']}")
                print(f"     Usage: {instance_usage['usage']}")
                print(f"     Pending Jobs: {instance_usage['pendingJobs']}")
                print(f"     Max Pending Jobs: {instance_usage['maxPendingJobs']}\n")

            print(' Selecting backend...')
            backend = service.least_busy(simulator=False, operational=True, min_num_qubits=bit_length)
            print("  Connected to the backend:")
            print(f"   Name: {backend.name}")
            print(f"   Version: {backend.backend_version}")
            print(f"   Number of Qubits: {backend.num_qubits}")
            print(f"   Local: {backend.local}")
            print(f"   Simulator: {backend.simulator}")
            print(f"   Conditional: {backend.conditional}")
            print(f"   Open Pulse: {backend.open_pulse}")
            print(f"   Memory: {backend.memory}")
            print(f"   Max Shots: {backend.max_shots}")
            print(f"   Dynamic Reprate Enabled: {backend.dynamic_reprate_enabled}")
            print(f"   Rep Delay Range: {backend.rep_delay_range}")
            print(f"   Default Rep Delay: {backend.default_rep_delay}")
            print(f"   Measurement Levels: {backend.meas_levels}")
            print(f"   Drive Channel Timestep (dt): {backend.dt} ns")
            print(f"   Measurement Channel Timestep (dtm): {backend.dtm} ns")
            print(f"   Rep Times: {backend.rep_times}")
            print(f"   Measurement Kernels: {backend.meas_kernels}")
            print(f"   Acquisition Latency: {backend.acquisition_latency}")
            print(f"   Conditional Latency: {backend.conditional_latency}")
            print(f"   Max Circuits: {backend.max_circuits}")
            print(f"   Sample Name: {backend.sample_name}")
            print(f"   Number of Registers: {backend.n_registers}")
            print(f"   Credits Required: {backend.credits_required}")
            print(f"   Online Date: {backend.online_date}")
            print(f"   Description: {backend.description}")
            print(f"   Version: {backend.version}")
            print(f"   Parametric Pulses: {backend.parametric_pulses}")
            print(f"   Processor Type: {backend.processor_type}\n")

        else:
            print("\n-- Enforcing AerSimulator usage -- ")
            backend = None


    except Exception as e:
        print(f" Failed to connect to IBM Quantum Runtime: {e}")
        print(" Falling back to AerSimulator...\n")
        backend = None

    qc = QuantumCircuit(bit_length)
    qc.h(range(bit_length))
    qc.measure_all()
    shots = 4096

    if backend:
        try:
            circ, counts = use_ibm_runtime(backend, qc, shots)
        
        except Exception as e:
            circ, counts = use_simulator(bit_length, qc, shots)

    else:
        circ, counts = use_simulator(bit_length, qc, shots)

    while True:
        if enhancement == "nth_count":            
            if nth_count > len(counts) or nth_count <= 0:
                print(f"   \nn-th count {nth_count} is out of range (max counts: {len(counts)}). Selecting the least populated outcome.")

                binary_result = min(counts, key=counts.get)

            else:
                binary_result = list(counts.keys())[nth_count - 1]  # Indexing starts at 0



            return circ, binary_result

        elif enhancement == "xor" and xor_value is not None:

            binary_result = random.choice(list(counts.keys()))
            random_number = int(binary_result, 2)

            random_number = random_number ^ xor_value # Basic XOR operator

            return circ, binary_result

        else:

            binary_result = random.choice(list(counts.keys()))

        return circ, binary_result

if __name__ == "__main__":
    print("\nWelcome to the Quantum Random Number Generator (QRNG)")
    print("Please ensure you have Qiskit and Qiskit IBM Runtime installed.")
    
    while True:
        bit_length = input("\nEnter the bit length for the random number (should be greater than 1, e.g., 32 or 64):\n ")
        bit_length = validate_positive_integer(bit_length)
        if bit_length and bit_length > 1:
            break
        print(" Invalid input. Please enter a positive integer greater than 1.")

    print("\nEnhancements available:")
    print(" 1. Use n-th result from the counts list.")
    print(" 2. XOR with a custom value.")
    print(" 3. None (default).")

    while True:
        enhancement_choice = input("\nChoose an enhancement (1, 2, or 3): ")
        if enhancement_choice in ["1", "2", "3"]:
            break
        print(" Invalid enhancement choice. Please choose 1, 2, or 3.")

    enhancement = None
    xor_value = None
    nth_count = 1

    if enhancement_choice == "1":
        enhancement = "nth_count"

        while True:
            nth_count = input(f"\n Enter a valid positive integer for the n-th result. Possible outcomes: {2 ** bit_length}: ")
            nth_count = validate_positive_integer( nth_count)

            if  nth_count is not None and 0 <  nth_count <= 2 ** bit_length:
                break

            print(f"  Invalid input. Please choose a number between 1 and {2 ** bit_length}.")

    elif enhancement_choice == "2":
        while True:
            xor_value = input(" Enter a valid positive integer to XOR with (the binary length of this number should match the specified bit length): ")
            xor_value = validate_positive_integer(xor_value)
            if xor_value:
                break
            print(" Invalid input. Please enter a positive integer.")
        enhancement = "xor"

    print(f" Selected enhancement: {enhancement}")

    force_using_simulator = None

    while True:
        force_using_simulator = input("\nForce to use simulator instead of QPU?:\n 0: No\n 1: Yes\n\nAnswer: ")

        if force_using_simulator in ("0","1"):
            force_using_simulator = int(force_using_simulator)
            break

        print(" Invalid input. Please enter 0 or 1")

    try:

        circ, quantum_bin  = generate_qrng(bit_length=bit_length,
                                            enhancement=enhancement,
                                            nth_count= nth_count,
                                            xor_value=xor_value,
                                            force_using_simulator=force_using_simulator)
        
        quantum_dec = int(quantum_bin, 2)
        quantum_hex = hex(quantum_dec)[2:]
        quantum_oct = oct(quantum_dec)[2:]

        print(f"\n--- Quantum RNG Results ---")
        print("Binary:      ", quantum_bin)
        print("Decimal:     ", quantum_dec)
        print("Hexadecimal: ", quantum_hex)
        print("Octal:       ", quantum_oct)
        print("Quantim Circuit used:",'\n')
        print(circ.draw(idle_wires=False))
        print('')

    except Exception as e:
        print('Error during RNG generation: ',e)