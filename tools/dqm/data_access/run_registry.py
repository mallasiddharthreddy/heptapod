"""
# run_registry.py — re-exports RunRegistryQueryTool from dqmio_reader module.
# Part of the HEPTAPOD package.
# Copyright (C) 2025 HEPTAPOD authors (see AUTHORS for details).
# HEPTAPOD is licensed under the GNU GPL v3 or later, see LICENSE for details.
"""

from tools.dqm.data_access.dqmio_reader import RunRegistryQueryTool

__all__ = ["RunRegistryQueryTool"]
