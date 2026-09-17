# ILP experiments

Requirements: Linux, gcc, Python 3, gem5 25.1.0.1 built for X86 with O3 CPU support.

Build workload:

    gcc -O2 -fno-tree-vectorize -static benchmark.c -o benchmark

Example simulation:

    /path/to/gem5.opt -d results/integer_w1 config.py --binary "$PWD/benchmark" --mode integer --width 1

Repeat for integer, floating, memory, and branch at widths 1 and 4. For the branch workload compare --predictor local with --predictor tournament. For SMT use --mode integer --width 4 --threads 2. Each x86 interrupt controller must be connected when multiple thread contexts are configured.

The experiment ZIP includes ilp/no_prediction. To build the non-adaptive control:

    scons build/X86/gem5.opt -j 12 EXTRAS=/absolute/path/to/ilp/no_prediction

Then use --predictor none. This returns fall-through for conditional direction decisions and never trains. BTB/RAS behavior for unconditional transfers is retained. It disables adaptive conditional-direction prediction, not all speculation or all target prediction; it is not a stall-until-resolution frontend.

Trace example:

    /path/to/gem5.opt -d results/trace --debug-flags=O3PipeView --debug-end=50000000 --debug-file=trace.out config.py --binary "$PWD/benchmark" --mode integer --width 1
    python3 /path/to/gem5/util/o3-pipeview.py -c 500 -o results/trace/pipeview.out results/trace/trace.out

At 2 GHz one cycle is 500 simulator ticks. IPC is architectural committed instructions/cycles. Fetch-to-retirement latency from O3PipeView concerns micro-operations, not necessarily whole x86 instructions. The bounded trace covers startup, not the complete kernel.

Full trace: omit --debug-end and use --debug-file=trace.out.gz. The complete local trace is about 80 MB compressed and is not committed to GitHub; raw configs/stats, a bounded visualizer trace, and full-run summary are included. Reproduce the full trace using the supplied workload/configuration before rerunning the latency parser.

Limitations: width changes the entire frontend/backend width bundle; libc startup and command dispatch are included; no calibrated power model is implemented. The O3 pipeline has more than five internal stages; its five functional roles are mapped explicitly in the report. Repository: https://github.com/hahajeera/MSCS531-Assignment4-ILP (private; instructor access must be arranged before grading).
