# TECHDUDES — QFF 2026 PS-O1 Technical Report



## Quantum Optimization of Network Partitioning Using QAOA



**Team:** TECHDUDES

**Challenge:** QFF 2026 — PS-O1

**Method:** Quantum Approximate Optimization Algorithm (QAOA), depth \(p=1\)



## Executive Summary



This project investigates weighted network partitioning as a Max-Cut optimization problem and evaluates a depth-\(p=1\) Quantum Approximate Optimization Algorithm (QAOA) implementation using ideal and noisy quantum simulation.



The six-vertex problem contains nine weighted edges. Exhaustive enumeration of all 64 possible assignments establishes an exact maximum-cut value of 22. QAOA parameters are optimized using five initializations, with seeds 0 through 4, and the selected parameters are evaluated using 4096 measurement shots.



Processor A has five physical qubits and cannot execute the six-logical-qubit problem. Processors B and D each provide nine physical qubits and are evaluated under ideal and noisy simulation conditions. Processor D uses a custom connected topology with twelve couplings and maximum degree three.



The observed mean cut values are 15.6606 and 15.4326 for Processor B under ideal and noisy conditions, respectively. For Processor D, the corresponding values are 15.5720 and 15.3633. The results show a reduction in mean cut under the configured noise model for both executable processors. Bell-state experiments also show lower noisy fidelity for the selected farthest pair than for the adjacent pair on Processor D.



All reported experiments are simulations. The results should be interpreted in the context of the selected problem instance, compilation settings, finite shot counts, optimizer, and noise model.



## 1. Objective and Problem Definition



The objective is to investigate quantum optimization for weighted network partitioning. In the Max-Cut formulation, each vertex is assigned to one of two groups. An edge contributes its weight to the cut when its endpoints belong to different groups.



Let \(x\_i\\in\\{0,1\\}\) denote the group assignment of vertex \(i\), and let \(w\_{ij}\) denote the weight of an edge between vertices \(i\) and \(j\). The cut objective is



\\\[

C(x)=\\sum\_{(i,j)\\in E}w\_{ij}|x\_i-x\_j|.

\\]



The goal is to find an assignment maximizing \(C(x)\). Equivalently, the QUBO cost used in this project is \(Q(x)=-C(x)\), so minimizing the QUBO is equivalent to maximizing the cut.



The instance has six vertices and nine weighted edges, with total edge weight 27. Exhaustive enumeration of the 64 possible bit assignments gives the exact optimum



\\\[

C^\*=22.

\\]



The optimal assignments in vertex order are `110100` and `001011`. These assignments are complements and describe the same partition with the two groups exchanged.



The exact solution provides a reference for assessing QAOA output. It also allows the approximation ratio and probability of sampling an optimal cut to be computed directly.



## 2. QAOA Method



QAOA alternates between a problem-dependent cost operation and a mixing operation. In this project, the circuit depth is \(p=1\), so the circuit uses one cost layer and one mixer layer controlled by two variational parameters, \(\\gamma\) and \(\\beta\).



The initial state is prepared using Hadamard gates on the six logical qubits. The cost layer encodes the weighted Max-Cut objective through edge-dependent interactions. The mixer applies single-qubit rotations. Measurement produces bitstrings that are converted into candidate partitions and evaluated using the weighted cut objective.



The parameter search uses five initializations with seeds 0, 1, 2, 3, and 4. Initial angles are sampled uniformly from \(\[0,\\pi]\) using NumPy's `default\_rng`. The optimizer uses the ideal statevector objective, and the selected parameters are subsequently evaluated with 4096 measurement shots and simulator seed 42.



This separates parameter optimization from finite-shot evaluation. Consequently, the reported measured mean cut need not equal the ideal expected cut used during optimization.



The main reported metrics are:



\- **Mean cut:** average cut value over the measured samples.

\- **Sample standard deviation:** spread of measured cut values.

\- **Approximation ratio:** mean sampled cut divided by the exact optimum.

\- **Best sampled cut:** highest cut observed among the measured samples.

\- **Optimal-cut probability:** fraction of samples attaining the exact optimum.



The approximation ratio is \(r=\\overline{C}/C^\*\). A ratio closer to one indicates a higher mean cut relative to the known optimum. The probability of sampling an optimal cut measures a different aspect of performance and should not be confused with the mean approximation ratio.



## 3. Processor Configurations and Experimental Setup



### 3.1 Processor A



Processor A has five physical qubits. Since the optimization problem requires six logical qubits, Processor A cannot execute the specified circuit without changing the problem representation. It is therefore reported as not executable for this benchmark. The six-vertex instance is not reduced to fit the smaller processor.



### 3.2 Processor B



Processor B has nine physical qubits and uses the supplied challenge topology. It is evaluated as the reference executable processor for the six-logical-qubit circuit.



### 3.3 Processor D



Processor D is a custom nine-qubit topology with twelve couplings. Its graph is connected and has maximum degree three. Its configured basis gates are `rz`, `sx`, `x`, and `cx`. The configuration is stored in `processors/processor\_D.json`.



The final Processor D configuration is the one used by the benchmark scripts. Keeping a single authoritative configuration is important because changes in connectivity or noise parameters can change routing, transpiled resources, and simulation outcomes.



### 3.4 Noise and Reproducibility



The configured noise parameters are single-qubit error probability \(p\_1=0.001\), two-qubit error probability \(p\_2=0.005\), and readout error probability \(p\_{\\mathrm{readout}}=0.01\). The simulator seed is 42 and final QAOA evaluations use 4096 shots.



The configured basis gates are `rz`, `sx`, `x`, and `cx`. The project also records processor configurations, result tables, scripts, and a Jupyter notebook to support inspection and rerunning the workflow.



These results depend on the configured simulator and noise model. They are not measurements from physical quantum hardware.



## 4. QAOA Results



The following table summarizes the measured results for the executable processors.



| Processor | Condition | Mean cut | Sample standard deviation | Approximation ratio | Best cut | Optimal-cut probability |

|---|---|---:|---:|---:|---:|---:|

| B | Ideal | 15.6606 | 4.0763 | 0.7118 | 22 | 0.0730 |

| B | Noisy | 15.4326 | 4.2065 | 0.7015 | 22 | 0.0698 |

| D | Ideal | 15.5720 | 4.1068 | 0.7078 | 22 | 0.0679 |

| D | Noisy | 15.3633 | 4.2813 | 0.6983 | 22 | 0.0671 |



Both executable processors sampled an optimal cut in their ideal and noisy evaluations. However, the optimal-cut probabilities are approximately 6.7% to 7.3%, meaning that most individual measurements did not produce an optimal assignment.



For Processor B, the mean cut decreases from 15.6606 under ideal simulation to 15.4326 under noisy simulation. Its approximation ratio decreases from approximately 0.7118 to 0.7015.



For Processor D, the mean cut decreases from 15.5720 to 15.3633, and the approximation ratio decreases from approximately 0.7078 to 0.6983. These changes are consistent with the effect of introducing the configured noise model, although the precise impact depends on the simulated circuit and finite-shot outcomes.



Processor B has a slightly higher measured mean cut than Processor D in both conditions in this experiment. This observation alone does not establish a universal ranking of the processor topologies. Different instances, compilation outcomes, noise assumptions, and parameter choices can lead to different results.



### 4.1 Random Baseline

The exact uniform-random baseline was calculated by enumerating all 64 assignments of the six-vertex graph. Each edge crosses the cut with probability \(1/2\), so the expected cut value is half the sum of all edge weights: \(27/2 = 13.5\). The exact maximum cut is 22, giving an expected approximation ratio of \(13.5/22 \approx 0.6136\).

For comparison, 4096 uniformly random assignments were also evaluated using seed 42. This sample had a mean cut of 13.5620 and a best observed cut of 22. The sampled mean is close to the exact expectation, as expected. Both baselines provide a reference for the selected instance; they do not establish that QAOA will outperform random sampling on every instance or under every experimental setting.


## 5. Circuit Resource Analysis



The compiled circuit resource measurements are summarized below.



| Processor | Logical CX count | Transpiled CX count | Circuit depth | Two-qubit depth | SWAP count | CX overhead |

|---|---:|---:|---:|---:|---:|---:|

| B | 18 | 21 | 37 | 17 | 1 | 3 |

| D | 18 | 24 | 37 | 18 | 2 | 6 |



The logical CX count is 18 for both executable processors. After compilation and routing, Processor B uses 21 CX gates, while Processor D uses 24. The corresponding CX overheads are three and six gates.



Processor D also has a two-qubit depth of 18, compared with 17 for Processor B, and uses two SWAP gates compared with one for Processor B. These measurements indicate that the tested Processor D circuit incurs additional routing overhead for this instance.



The resource results help explain why connectivity matters when mapping logical circuits onto physical topologies. They should be interpreted together with the measured cut quality and noise assumptions rather than as an independent measure of overall processor quality.



Processor A is excluded from the executable resource comparison because it cannot accommodate the required six logical qubits.



## 6. Bell-State Experiments on Processor D



Bell-state experiments were performed for an adjacent pair, \((0,1)\), and a selected farthest pair, \((0,8)\). Each experiment used 4096 shots per measurement basis and condition. The reported correlations are \(XX\), \(YY\), and \(ZZ\); the Bell-state fidelity is computed from these correlations.



For the ideal adjacent pair, the correlations are \(XX=1.0000\), \(YY=-1.0000\), and \(ZZ=1.0000\), with fidelity 1.0000. The ideal farthest-pair results have the same correlations and fidelity.



Under noisy simulation, the adjacent-pair results are:



\- \(XX=0.9458\), standard error 0.0051.

\- \(YY=-0.9521\), standard error 0.0048.

\- \(ZZ=0.9551\), standard error 0.0046.

\- Fidelity \(=0.9633\), standard error 0.0021.



For the farthest pair, the noisy results are:



\- \(XX=0.9219\), standard error 0.0061.

\- \(YY=-0.9077\), standard error 0.0066.

\- \(ZZ=0.9385\), standard error 0.0054.

\- Fidelity \(=0.9420\), standard error 0.0026.



The noisy farthest-pair fidelity is lower than the noisy adjacent-pair fidelity in this simulation. The farthest-pair circuit also uses ten CX gates, compared with one for the adjacent pair. This is consistent with greater routing and gate exposure for the longer interaction path under the configured model.



The ideal results provide a reference showing the expected correlations in the absence of modeled noise. The noisy results quantify the reduction observed in this setup. The reported standard errors describe finite-shot uncertainty; they do not account for every possible modeling or implementation uncertainty.



The full Bell-test table, including correlations, standard errors, fidelities, and CX counts, is saved in `results/tables/bell.csv`.



## 7. Initialization Stability



Five QAOA initializations were evaluated using seeds 0 through 4. The mean ideal expected cut across these initializations was 15.5257, and the mean approximation ratio was 0.7057.



The population standard deviation of the five approximation ratios was approximately 0.00125. Seed 2 achieved the highest ideal expected-cut ratio among the five tested initializations.



The small spread suggests that these five runs produced similar ideal objective values. Nevertheless, five initializations are a limited sample and do not establish that the optimizer found a global optimum of the QAOA parameter landscape. Different seeds, optimizers, stopping criteria, or circuit depths may produce different outcomes.



The initialization records and summary are available in `results/tables/initialization\_summary.csv` and the associated initialization results file.



## 8. Reproducibility, Limitations, and Future Work



The project stores the problem instance in `data/instance.json`, processor configurations in `processors/`, experiment outputs in `results/`, and the notebook in `main.ipynb`. The pinned Python dependencies are listed in `requirements.txt`.



For reproducibility, the workflow should be rerun from a clean environment using the documented dependencies. The notebook should be executed from the repository root, and the output tables should be checked against the saved experiment results. Processor D must be validated using the final file in `processors/processor\_D.json` before benchmarking.



Several limitations should be considered:



1\. The QAOA circuit uses \(p=1\), which limits the expressiveness of the variational circuit.

2\. The optimization study uses five initializations and does not establish global optimality of the variational parameters.

3\. Final evaluations use finite shot counts, so measured means, standard deviations, and optimal-cut probabilities are subject to sampling variability.

4\. The noise model is a simulation configuration and may not capture all behavior of physical quantum hardware.

5\. The results apply to one six-vertex weighted graph and should not be generalized to arbitrary network partitioning instances.

6\. Circuit resource counts depend on the selected topology, compilation procedure, and transpiler settings.



Potential future work includes evaluating deeper QAOA circuits, testing additional parameter initializations, studying alternative connected Processor D topologies, and comparing results across additional weighted graphs. Such extensions should be reported as new experiments rather than inferred from the present results.



## 9. Conclusion



This project implements and evaluates depth-\(p=1\) QAOA for a six-vertex weighted Max-Cut instance with exact optimum 22. Processors B and D both sampled an optimal cut under ideal and noisy simulation, while their mean cut values and optimal-cut probabilities decreased under the configured noise model.



Processor B had a slightly higher mean cut and lower compiled CX count than Processor D in the reported experiment. Processor D's Bell-state experiments showed lower noisy fidelity for the selected farthest pair than for the adjacent pair. These findings demonstrate how topology, routing, noise, and finite-shot sampling affect the observed results in this simulation.



Processor A cannot execute the six-logical-qubit circuit because it has only five physical qubits. The project preserves the original problem rather than substituting a reduced instance.



Overall, the experiment provides a reproducible simulation-based comparison of solution quality, circuit resources, and Bell-state behavior for the selected processor configurations. The results should be interpreted within the stated experimental limitations.



## 10. AI-Use Disclosure



AI assistance was used to support development guidance, debugging, experimental workflow organization, and preparation and editing of project documentation. The team reviewed the resulting code, configuration files, and reported results against the project's execution outputs. The team remains responsible for the submitted implementation, experimental results, interpretation, and final report.
