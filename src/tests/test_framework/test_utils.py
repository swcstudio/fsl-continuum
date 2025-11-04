"""
FSL Continuum - Test Utils Module

Re-exports BasicTestUtils (as TestUtils) from base_test_class for backward compatibility.
"""

from .base_test_class import BasicTestUtils as TestUtils

__all__ = ['TestUtils']
