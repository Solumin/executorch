# -*- coding: utf-8 -*-
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
SDK Integration Tutorial
========================

**Author:** `Jack Khuu <https://github.com/Jack-Khuu>`__
"""

######################################################################
# The `ExecuTorch SDK <../sdk-overview.html>`__ is a set of tools designed to
# provide users with the ability to profile, debug, and visualize ExecuTorch
# models.
#
# This tutorial will show a full end-to-end flow of how to utilize the SDK.
# Specifically, it will:
#
# 1. Generate the artifacts consumed by the SDK (`ETRecord <../sdk-etrecord>`__, `ETDump <../sdk-etdump.html>`__).
# 2. Create an Inspector class consuming these artifacts.
# 3. Utilize the Inspector class to analyze the model.

######################################################################
# Prerequisites
# -------------
#
# To run this tutorial, you’ll need to install ExecuTorch.
#
# Set up a conda environment. To set up a conda environment in Google Colab::
#
#   !pip install -q condacolab
#   import condacolab
#   condacolab.install()
#
#   !conda create --name executorch python=3.10
#   !conda install -c conda-forge flatbuffers
#
# Install ExecuTorch from source. If cloning is failing on Google Colab, make
# sure Colab -> Setting -> Github -> Access Private Repo is checked::
#
#   !git clone https://{github_username}:{token}@github.com/pytorch/executorch.git
#   !cd executorch && bash ./install_requirements.sh

######################################################################
# Generate ETRecord (Optional)
# ----------------------------
#
# The first step is to generate an ``ETRecord``. ``ETRecord`` contains model
# graphs and metadata for linking runtime results (such as profiling) to
# the eager model. This is generated via ``executorch.sdk.generate_etrecord``.
#
# ``executorch.sdk.generate_etrecord`` takes in an output file path (str), the
# edge dialect model (ExirExportedProgram), the ExecuTorch dialect model
# (ExecutorchProgram), and an optional dictionary of additional models
#
# In this tutorial, the mobilenet v2 example model is used to demonstrate::
#
#   # Imports
#   import copy
#
#   import torch
#
#   from executorch import exir
#   from executorch.examples.models.mobilenet_v2 import MV2Model
#   from executorch.exir import ExecutorchProgram, ExirExportedProgram, ExportedProgram
#   from executorch.sdk import generate_etrecord
#
#   # Generate MV2 Model
#   model: torch.nn.Module = MV2Model()
#   aten_model: ExportedProgram = exir.capture(
#       model.get_eager_model().eval(),
#       model.get_example_inputs(),
#       exir.CaptureConfig(),
#   )
#
#   edge_model: ExirExportedProgram = aten_model.to_edge(
#       exir.EdgeCompileConfig(_check_ir_validity=True)
#   )
#   edge_copy: ExirExportedProgram = copy.deepcopy(edge_model)
#
#   et_model: ExecutorchProgram = edge_model.to_executorch()
#
#   # Generate ETRecord
#   etrecord_path = "etrecord.bin"
#   generate_etrecord(etrecord_path, edge_copy, et_model)
#

######################################################################
# Generate ETDump
# ---------------
#
# Next step is to generate an ``ETDump``. ``ETDump`` contains runtime results
# from executing the model. To generate, simply pass the ExecuTorch model
# to the ``executor_runner``::
#
#   buck2 run executorch/examples/export:export_example -- -m mv2
#   buck2 run @mode/opt -c executorch.event_tracer_enabled=true executorch/sdk/runners:executor_runner -- --model_path mv2.pte
#
# TODO: Add Instructions for CMake, when landed

######################################################################
# Creating an Inspector
# ---------------------
#
# Final step is to create the ``Inspector`` by passing in the artifact paths.
# Inspector takes the runtime results from ``ETDump`` and correlates them to
# the operators of the Edge Dialect Graph.
#
# Note: An ``ETRecord`` is not required. If an ``ETRecord`` is not provided,
# the Inspector will show runtime results without operator correlation.
#
# To visualize all runtime events, call ``print_data_tabular``::
#
#   from executorch.sdk import Inspector
#
#   etdump_path = "etdump.etdp"
#   inspector = Inspector(etdump_path=etdump_path, etrecord_path=etrecord_path)
#   inspector.print_data_tabular()
#

######################################################################
# Conclusion
# ----------
#
# In this tutorial, we learned about the steps required to consume an ExecuTorch
# model with the ExecuTorch SDK. It also showed how to use the Inspector APIs
# to analyze the model run results.
#
# Links Mentioned
# ^^^^^^^^^^^^^^^
#
# - `ExecuTorch SDK <../sdk-overview.html>`__
# - `ETRecord <../sdk-etrecord>`__
# - `ETDump <../sdk-etdump.html>`__
