from setuptools import find_packages, setup

setup(
    name="pizza_shop",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        # Add your project's dependencies here
    ],
    # Optional: Add test dependencies
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
        ],
    },
)
