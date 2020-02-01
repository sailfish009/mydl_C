## Installation

Our [Colab Notebook](https://colab.research.google.com/drive/16jcaJoc6bCFAQ96jDe2HwtXj7BMD_-m5)
has step-by-step instructions that install mydl.
The [Dockerfile](https://github.com/facebookresearch/mydl/blob/master/docker/Dockerfile)
also installs mydl with a few simple commands.

### Requirements
- Linux or macOS
- Python ≥ 3.6
- PyTorch ≥ 1.3
- [torchvision](https://github.com/pytorch/vision/) that matches the PyTorch installation.
	You can install them together at [pytorch.org](https://pytorch.org) to make sure of this.
- OpenCV, optional, needed by demo and visualization
- pycocotools: `pip install cython; pip install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'`
- gcc & g++ ≥ 4.9


### Build and Install Detectron2

After having the above dependencies, run:
```
pip install 'git+https://github.com/facebookresearch/mydl.git'
# (add --user if you don't have permission)

# Or, to install it from a local clone:
git clone https://github.com/facebookresearch/mydl.git
cd mydl && pip install -e .

# Or if you are on macOS
# MACOSX_DEPLOYMENT_TARGET=10.9 CC=clang CXX=clang++ pip install -e .
```

To __rebuild__ mydl that's built from a local clone, `rm -rf build/ **/*.so` then `pip install -e .`.
You often need to rebuild mydl after reinstalling PyTorch.

### Common Installation Issues

Click each issue for its solutions:

<details>
<summary>
Undefined torch/aten/caffe2 symbols, or segmentation fault immediately when running the library.
</summary>

This can happen if mydl or torchvision is not
compiled with the version of PyTorch you're running.

If you use a pre-built torchvision, uninstall torchvision & pytorch, and reinstall them
following [pytorch.org](http://pytorch.org).
If you manually build mydl or torchvision, remove the files you built (`build/`, `**/*.so`)
and rebuild them.

If you cannot resolve the problem, please include the output of `gdb -ex "r" -ex "bt" -ex "quit" --args python -m mydl.utils.collect_env`
in your issue.
</details>

<details>
<summary>
Undefined C++ symbols in `mydl/_C*.so`.
</summary>
Usually it's because the library is compiled with a newer C++ compiler but run with an old C++ run time.
This can happen with old anaconda.

Try `conda update libgcc`. Then rebuild mydl.
</details>

<details>
<summary>
"Not compiled with GPU support" or "Detectron2 CUDA Compiler: not available".
</summary>
CUDA is not found when building mydl.
You should make sure

```
python -c 'import torch; from torch.utils.cpp_extension import CUDA_HOME; print(torch.cuda.is_available(), CUDA_HOME)'
```

print valid outputs at the time you build mydl.
</details>

<details>
<summary>
"invalid device function" or "no kernel image is available for execution".
</summary>

Two possibilities:

* You build mydl with one version of CUDA but run it with a different version.

  To check whether it is the case,
  use `python -m mydl.utils.collect_env` to find out inconsistent CUDA versions.
	In the output of this command, you should expect "Detectron2 CUDA Compiler", "CUDA_HOME", "PyTorch built with - CUDA"
	to contain cuda libraries of the same version.

	When they are inconsistent,
	you need to either install a different build of PyTorch (or build by yourself)
	to match your local CUDA installation, or install a different version of CUDA to match PyTorch.

* Detectron2 or PyTorch/torchvision is not built for the correct GPU architecture (compute compatibility).

	The GPU architecture for PyTorch/mydl/torchvision is available in the "architecture flags" in
	`python -m mydl.utils.collect_env`.

	The GPU architecture flags of mydl/torchvision by default matches the GPU model detected
	during building. This means the compiled code may not work on a different GPU model.
	To overwrite the GPU architecture for mydl/torchvision, use `TORCH_CUDA_ARCH_LIST` environment variable during building.

	For example, `export TORCH_CUDA_ARCH_LIST=6.0,7.0` makes it work for both P100s and V100s.
	Visit [developer.nvidia.com/cuda-gpus](https://developer.nvidia.com/cuda-gpus) to find out
	the correct compute compatibility number for your device.

</details>

<details>
<summary>
Undefined CUDA symbols or cannot open libcudart.so.
</summary>

The version of NVCC you use to build mydl or torchvision does
not match the version of CUDA you are running with.
This often happens when using anaconda's CUDA runtime.

Use `python -m mydl.utils.collect_env` to find out inconsistent CUDA versions.
In the output of this command, you should expect "Detectron2 CUDA Compiler", "CUDA_HOME", "PyTorch built with - CUDA"
to contain cuda libraries of the same version.

When they are inconsistent,
you need to either install a different build of PyTorch (or build by yourself)
to match your local CUDA installation, or install a different version of CUDA to match PyTorch.
</details>


<details>
<summary>
"ImportError: cannot import name '_C'".
</summary>
Please build and install mydl following the instructions above.
</details>
