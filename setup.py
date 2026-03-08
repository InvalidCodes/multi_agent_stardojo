# setup.py
from setuptools import setup, find_packages

setup(
    name="stardojo",
    version="0.1.0",
    description="StarDojo - Stardew Valley AI Agent Framework",
    author="StarDojo Team",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.20.0",
        "gymnasium>=0.28.0",
        "pygame>=2.0.0",
        "pillow>=9.0.0",
        "pyyaml>=6.0",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "msgpack>=1.0.0",
            "opencv-python>=4.10.0",
            "backoff==2.2.1",
            "spacy>=3.8.0",
            "mss>=7.1.0",
            "spicy>=0.2.1",
            "supervison",
            "pyautogui>=0.9.55",
            "ahk[binary]>=0.1.1",
            "pydirectinput>=0.5.0",
        ],
        "llm": [
            "anthropic>=0.18.0",
            "openai>=1.0.0",
            "google-genai>=0.10.0",
        ]
    }
)