from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README-PIP.md").read_text()

setup(
    name="ggallery",
    version="1.0.9",
    description="A tool to generate static HTML photo galleries from various data sources.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Radzivon Chorny",
    author_email="mityy2012@gmail.com",
    url="https://github.com/creeston/ggallery",
    packages=find_packages(),
    include_package_data=True,  # Include non-Python files (e.g., templates)
    install_requires=[
        "azure-storage-blob==12.24.1",
        "Pillow==11.1.0",
        "Jinja2==3.1.5",
        "PyYAML==6.0.2",
        "python-dotenv==1.0.1",
        "pydantic==2.10.6",
        "docker==7.1.0",
    ],
    entry_points={
        "console_scripts": [
            "ggallery=ggallery.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    project_urls={
        "Documentation": "https://github.com/creeston/ggallery",
        "Source": "https://github.com/creeston/ggallery",
        "Tracker": "https://github.com/creeston/ggallery/issues",
    },
    keywords="static html photo gallery generator",
)
