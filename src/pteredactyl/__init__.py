# read version from installed package
from importlib.metadata import version

__version__ = version("pteredactyl")
import sys
import warnings

import torch

from pteredactyl.defaults import (
    DEFAULT_ENTITIES,  # noqa: F401
    DEFAULT_NER_MODEL,  # noqa: F401
    DEFAULT_REGEX_ENTITIES,  # noqa: F401
    DEFAULT_SPACY_MODEL,  # noqa: F401
    show_defaults,  # noqa: F401
)  # noqa: F401
from pteredactyl.redactor import (  # noqa: F401
    analyse,
    anonymise,
    anonymise_df,
    create_analyser,
)
from pteredactyl.regex_entities import build_pteredactyl_recogniser  # noqa: F401

if not torch.cuda.is_available():
    base_message = "CUDA is not installed, so pteredactyl will use CPU rather than GPU."
    full_version = sys.version
    minor_version = sys.version_info.minor
    end_message = (
        f""" -> Note that CUDA installation currently requires Python <= 3.12, so you will need to downgrade your Python version to use it.
 -> Current python version: {full_version}"""
        if minor_version > 12
        else ""
    )

    warnings.warn(
        f"""
{base_message}
 -> You can install CUDA 12.1 by running: pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --upgrade
 -> Alternatively to select a compatible version visit: https://pytorch.org/get-started/locally/ and generate a pip3 installation command
{end_message}""",
        stacklevel=2,
    )
