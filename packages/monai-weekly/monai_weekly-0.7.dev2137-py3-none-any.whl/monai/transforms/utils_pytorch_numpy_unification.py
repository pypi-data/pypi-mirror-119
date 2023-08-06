# Copyright 2020 - 2021 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import torch

from monai.config.type_definitions import NdarrayOrTensor

__all__ = [
    "moveaxis",
    "in1d",
]


def moveaxis(x: NdarrayOrTensor, src: int, dst: int) -> NdarrayOrTensor:
    """`moveaxis` for pytorch and numpy, using `permute` for pytorch ver < 1.8"""
    if isinstance(x, torch.Tensor):
        if hasattr(torch, "moveaxis"):
            return torch.moveaxis(x, src, dst)
        return _moveaxis_with_permute(x, src, dst)  # type: ignore
    if isinstance(x, np.ndarray):
        return np.moveaxis(x, src, dst)
    raise RuntimeError()


def _moveaxis_with_permute(x, src, dst):
    # get original indices
    indices = list(range(x.ndim))
    # make src and dst positive
    if src < 0:
        src = len(indices) + src
    if dst < 0:
        dst = len(indices) + dst
    # remove desired index and insert it in new position
    indices.pop(src)
    indices.insert(dst, src)
    return x.permute(indices)


def in1d(x, y):
    """`np.in1d` with equivalent implementation for torch."""
    if isinstance(x, np.ndarray):
        return np.in1d(x, y)
    return (x[..., None] == torch.tensor(y, device=x.device)).any(-1).view(-1)
