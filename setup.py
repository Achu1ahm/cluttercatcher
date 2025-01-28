    form setup import setup, find_packages

    setup(
        name="clutter-catcher",
        version="0.1.0",
        author="Asfaq Ahmed",
        author_email="asfaqahmed128@gmail.com",
        description="A tool to clean unused files, imports, and dependencies from projects.",
        long_description=open("README.md").read(),long_description_content_type="text/markdown",
        url="https://github.com/Achu1ahm/cluttercatcher",packages=find_packages(),
        python_requires=">=3.7",
        install_requires=[],
        entry_points={
        "console_scripts": [
            "cluttercatcher=cluttercatcher.cli:main",
        ],
    },
    )