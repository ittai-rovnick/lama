"""Setup configuration for LAMA^AI Loan Exchange Service"""

from setuptools import setup, find_packages

with open("docs/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lama-exchange",
    version="1.0.0",
    author="LAMA^AI Inc.",
    description="Loan Exchange Service - Match loan applications with eligible lenders",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lama-ai/loan-exchange",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "httpx>=0.25.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ]
    },
)
