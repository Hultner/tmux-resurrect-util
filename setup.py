from setuptools import setup

setup(
    name="tmux-res",
    version="0.3",
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
