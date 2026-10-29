# TECHDUDES — QFF 2026 PS-O1 Technical Report

## 1. Objective

This project studies weighted Max-Cut using the Quantum Approximate Optimization Algorithm (QAOA) at depth p = 1. It compares ideal and noisy simulation results for Processors B and D and documents why Processor A cannot execute the six-qubit logical circuit.

## 2. Problem instance

The graph contains six vertices and nine weighted edges, with total edge weight 27. Exhaustive enumeration of all 64 bit assignments gives an exact maximum-cut value of 22.

The optimal assignments, in vertex order, are 110100 and 001011. Complementary assignments represent the same cut.

## 3. Method

The QAOA circuit uses depth p = 1. Five parameter initializations use random seeds 0 through 4, with initial angles sampled uniformly from [0, pi]. The optimizer uses the ideal statevector objective. The selected parameters are then evaluated with 4096 measurement shots and simulator seed 42.

The reported approximation ratio is the mean sampled cut divided by the exact optimum. The optimal-cut probability is the fraction of measured samples achieving the exact optimum.

## 4. Processor configurations

Processor A has five physical qubits and cannot execute the six-logical-qubit circuit. It is therefore reported as not executable rather than being evaluated on a reduced problem.

Processor B has nine qubits and uses the supplied challenge topology. Processor D has nine qubits and twelve couplings. Its topology is connected and has maximum degree three. Its configured basis gates are rz, sx, x, and cx.

The Processor D configuration is stored in processors/processor_D.json and is the configuration used by the benchmark scripts.

## 5. QAOA results

| Processor | Condition | Mean cut | Sample standard deviation | Approximation ratio | Best cut | Optimal-cut probability |
|---|---|---:|---:|---:|---:|---:|
| B | Ideal | 15.6606 | 4.0763 | 0.7118 | 22 | 0.0730 |
| B | Noisy | 15.4326 | 4.2065 | 0.7015 | 22 | 0.0698 |
| D | Ideal | 15.5720 | 4.1068 | 0.7078 | 22 | 0.0679 |
| D | Noisy | 15.3633 | 4.2813 | 0.6983 | 22 | 0.0671 |

Both executable processors sampled an optimal cut in their ideal and noisy runs. This does not mean every run finds the optimum; the optimal-cut probabilities are approximately 6.7% to 7.3%.

The random baseline used 4096 uniformly random assignments. Its observed mean cut was 13.5620, and its best cut was 22. The baseline is a reference point, not a guarantee that every random run performs similarly.

## 6. Circuit resources

| Processor | Logical CX count | Transpiled CX count | Circuit depth | Two-qubit depth | SWAP count | CX overhead |
|---|---:|---:|---:|---:|---:|---:|
| B | 18 | 21 | 37 | 17 | 1 | 3 |
| D | 18 | 24 | 37 | 18 | 2 | 6 |

Processor D uses three more CX gates and one more unit of two-qubit depth than Processor B in these compiled circuits. Its noisy mean cut is also lower in this experiment. These results alone do not establish that one processor is universally better; performance depends on the topology, compilation, noise model, and instance.

## 7. Bell-test results

Bell tests were run on an adjacent pair (0, 1) and a farthest pair (0, 8) of Processor D, with 4096 shots per basis and condition.

| Pair | Condition | CX count | XX | YY | ZZ | Fidelity |
|---|---|---:|---:|---:|---:|---:|
| (0, 1) | Ideal | 1 | 1.0000 | -1.0000 | 1.0000 | 1.0000 |
| (0, 1) | Noisy | 1 | 0.9458 | -0.9521 | 0.9551 | 0.9633 |
| (0, 8) | Ideal | 10 | 1.0000 | -1.0000 | 1.0000 | 1.0000 |
| (0, 8) | Noisy | 10 | 0.9219 | -0.9077 | 0.9385 | 0.9420 |

The noisy farthest-pair Bell test has lower fidelity than the adjacent-pair test in this simulation. This is consistent with the longer compiled interaction path and greater exposure to modeled errors. The full standard errors are recorded in results/tables/bell.csv.

## 8. Initialization stability

Five initializations were evaluated. Their mean ideal expected cut was 15.5257, with mean approximation ratio 0.7057. The population standard deviation of the five ratios was 0.00125. Seed 2 had the highest ideal expected-cut ratio among these five initializations.

This is a small initialization study and does not establish a global optimum of the QAOA parameter landscape.

## 9. Reproducibility and limitations

The experiment outputs are saved under results/. The processor configurations are saved under processors/, and the problem instance is saved under data/instance.json.

The reported results are simulated results, not physical-hardware measurements. They depend on the selected optimizer, finite shot counts, transpilation, simulator seeds, and configured noise model. The notebook should be run from a clean environment using requirements.txt to verify the workflow before submission.

## 10. AI-use disclosure

AI assistance was used for development guidance, debugging, and preparation of project documentation. The team should review this statement and amend it as necessary to accurately disclose all assistance used.
