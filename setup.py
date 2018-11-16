#!usr/bin/env sh

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name="tmux-res",
    author="Alexander Hultnér",
    author_email="ahultner@gmail.com",
    description="Handles your tmux resurrect files",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="0.4.8",
    py_modules=["app"],
    install_requires=["Click", "python-dotenv"],
    entry_points="""
        [console_scripts]
        tmux-res=app:cli
    """,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.7",
)
