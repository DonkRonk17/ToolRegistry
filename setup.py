#!/usr/bin/env python3
"""
Setup script for ToolRegistry.

Install in development mode:
    pip install -e .

Then use from anywhere:
    toolregistry scan
    toolregistry search synapse
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "ToolRegistry - Unified Tool Discovery for Team Brain"

setup(
    name="toolregistry",
    version="1.0.0",
    author="Forge (Team Brain)",
    author_email="logan@metaphy.dev",
    description="Unified Tool Discovery and Management for Team Brain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonkRonk17/ToolRegistry",
    py_modules=["toolregistry"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "toolregistry=toolregistry:main",
        ],
    },
    keywords="tools, discovery, registry, catalog, team-brain, ai-agents",
    project_urls={
        "Bug Reports": "https://github.com/DonkRonk17/ToolRegistry/issues",
        "Source": "https://github.com/DonkRonk17/ToolRegistry",
        "Documentation": "https://github.com/DonkRonk17/ToolRegistry#readme",
    },
)
