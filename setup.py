#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="quizcraft",
    version="0.1.0",
    description="A tool to extract and generate quiz questions from PDFs",
    author="QuizCraft Team",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "quizcraft=quizcraft.main:main",
        ],
    },
    python_requires=">=3.8",
)