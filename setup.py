from setuptools import setup

setup(
    name="aminodorks.py",
    version="0.0.1b10",
    description="Amino API wrapper and tools",
    author="Nullable-developer",
    author_email="nulllable@proton.me",
    install_requires=[
        "httpx>=0.25.0",
        "aiofiles>=23.0.0",
        "msgspec>=0.17.0",
        "orjson >= 3.10.16"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.10",
)