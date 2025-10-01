"""
This module provides a debug utility to print paths and font information
related to the PDF generation assets.
"""

from .paths import ASSETS, ICONS_DIR
from .fonts import _AR_NAME, _AR_PATH, _UI_NAME, _UI_PATH


def print_assets_info():
    """Prints asset and font information for debugging purposes."""
    print("ASSETS:", ASSETS)
    print("ICONS_DIR:", ICONS_DIR)
    print("Arabic font:", _AR_NAME, _AR_PATH)
    print("Symbols font:", _UI_NAME, _UI_PATH)