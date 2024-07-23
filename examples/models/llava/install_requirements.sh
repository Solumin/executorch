#!/bin/bash
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

set -x

# install llava from the submodule. We can't do pip install llava because it is packaged incorrectly.
pip install --force-reinstall -e examples/third-party/LLaVA

# not included in the pip install package, but needed in llava
pip install protobuf

# bitsandbytes depends on numpy 1.x, which is not compatible with numpy 2.x.
# Reinstall bitsandbytes to make it compatible.
pip install bitsandbytes -I

# numpy needs to be pin to 1.24. 1.26.4 will error out: Could not infer dtype of numpy.uint8
# On macos, numpy 1.24 is not available, 1.26.4 works fine.
pip install numpy==1.24

# The deps of llava can have different versions than deps of ExecuTorch.
# For example, torch version required from llava is older than ExecuTorch.
# To make both work, recover ExecuTorch's original dependencies by rerunning
# the install_requirements.sh. Notice this won't install executorch.
bash -x ./install_requirements.sh --deps-only

# Newer transformer (4.48) will give TypeError: LlavaLlamaForCausalLM.forward() got an unexpected keyword argument 'cache_position'
pip install timm==0.6.13
pip install transformers==4.37.2
