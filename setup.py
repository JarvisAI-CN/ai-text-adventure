"""
Setup script for AI Text Adventure
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-text-adventure",
    version="1.0.0",
    author="JarvisAI-CN",
    author_email="fishel.shuai@gmail.com",
    description="An AI-powered text adventure game with dynamic storytelling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JarvisAI-CN/ai-text-adventure",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Role-Playing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ai-text-adventure=src.cli:main",
        ],
    },
    keywords="ai game text-adventure rpg interactive-fiction",
    project_urls={
        "Bug Reports": "https://github.com/JarvisAI-CN/ai-text-adventure/issues",
        "Source": "https://github.com/JarvisAI-CN/ai-text-adventure",
    },
)
