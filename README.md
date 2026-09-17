# ILP experiments

Requirements: Linux, gcc, Python 3, gem5 25.1.0.1 built for X86 with O3 CPU support.

Build workload:

    gcc -O2 -fno-tree-vectorize -static benchmark.c -o benchmark

Example simulation:

    /path/to/gem5.opt -d results/integer_w1 config.py --binary "$PWD/benchmark" --mode integer --width 1

Repeat for integer, floating, memory, and branch at widths 1 and 4. For the branch workload compare --predictor local with --predictor tournament. For SMT use --mode integer --width 4 --threads 2. Each x86 interrupt controller must be connected when multiple thread contexts are configured.

Trace example:

    /path/to/gem5.opt -d results/trace --debug-flags=O3PipeView --debug-end=50000000 --debug-file=trace.out config.py --binary "$PWD/benchmark" --mode integer --width 1
    python3 /path/to/gem5/util/o3-pipeview.py -c 500 -o results/trace/pipeview.out results/trace/trace.out

At 2 GHz one cycle is 500 simulator ticks. IPC is architectural committed instructions/cycles. Fetch-to-retirement latency from O3PipeView concerns micro-operations, not necessarily whole x86 instructions. The bounded trace covers startup, not the complete kernel.

Limitations: width changes the entire frontend/backend width bundle; libc startup and command dispatch are included; both supplied predictors are dynamic; no prediction-disabled control or calibrated power model is implemented. Repository: https://github.com/hahajeera/MSCS531-Assignment4-ILP (private; instructor access must be arranged before grading).
