# ///////////////////////////////////////////////////////////////
# FLASH_EXCEL - Main Module
# Project: flash-excel
# ///////////////////////////////////////////////////////////////

"""flash-excel - Desktop utility to transform Excel/CSV files via TOML presets."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Local imports
from ._version import __version__

# ///////////////////////////////////////////////////////////////
# METADATA INFORMATION
# ///////////////////////////////////////////////////////////////

__author__ = "Neuraaak"
__maintainer__ = "Neuraaak"
__description__ = (
    "flash-excel - Desktop utility to transform Excel/CSV files via TOML presets"
)
__python_requires__ = ">=3.13"
__keywords__ = [
    "excel",
    "csv",
    "data",
    "transformation",
    "pipeline",
    "toml",
    "polars",
    "desktop",
]
__url__ = "https://github.com/neuraaak/flash-excel"
__repository__ = "https://github.com/neuraaak/flash-excel"

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////

__all__ = ["__version__"]
