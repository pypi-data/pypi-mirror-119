Highlights:
   - **CUDA backend**
      - Wrap the default profiling tool as EventToolkit , add a new class for CUPTI toolkit (#2916) (by **rocket**)
      - Add traced_records_ for KernelProfilerBase, refactoring KernelProfilerCUDA::sync() (#2909) (by **rocket**)
      - Move KernelProfilerCUDA from program/kernel_profiler.cpp to backends/cuda/cuda_profiler.cpp (#2902) (by **rocket**)
      - Add a compilation option for CUDA toolkit (#2899) (by **rocket**)
   - **Documentation**
      - Add docstring for indices() and axes() (#2917) (by **Ye Kuang**)

Full changelog:
   - Disable a few vulkan flaky tests. (#2926) (by **Ailing**)
   - [llvm] Remove duplicated set dim attribute for GlobalVariableExpression (#2929) (by **Ailing**)
   - [ci] Artifact uploading before test in release.yml (#2921) (by **Jiasheng Zhang**)
   - [bug] Fix the Bug that cannot assign a value to a scalar member in a struct from python scope (#2894) (by **JeffreyXiang**)
   - [misc] Update examples (#2924) (by **Taichi Gardener**)
   - [ci] Enable tmate session if release test fails. (#2919) (by **Ailing**)
   - [refactor] [CUDA] Wrap the default profiling tool as EventToolkit , add a new class for CUPTI toolkit (#2916) (by **rocket**)
   - [metal] Fix upperbound for list-gen and struct-for (#2915) (by **Ye Kuang**)
   - [ci] Fix linux release forgot to remove old taichi (#2914) (by **Jiasheng Zhang**)
   - [Doc] Add docstring for indices() and axes() (#2917) (by **Ye Kuang**)
   - [refactor] Rename SNode::n to SNode::num_cells_per_container (#2911) (by **Ye Kuang**)
   - Enable deploy preview if changes are detected in docs. (#2913) (by **Ailing**)
   - [refactor] [CUDA] Add traced_records_ for KernelProfilerBase, refactoring KernelProfilerCUDA::sync() (#2909) (by **rocket**)
   - [ci] Moved linux release to github action (#2905) (by **Jiasheng Zhang**)
   - [refactor] [CUDA] Move KernelProfilerCUDA from program/kernel_profiler.cpp to backends/cuda/cuda_profiler.cpp (#2902) (by **rocket**)
   - [wasm] Fix WASM AOT module builder order (#2904) (by **Ye Kuang**)
   - [CUDA] Add a compilation option for CUDA toolkit (#2899) (by **rocket**)
   - [vulkan] Support for multiple SNode trees in Vulkan (#2903) (by **Dunfan Lu**)
   - add destory snode tree api (#2898) (by **Dunfan Lu**)
