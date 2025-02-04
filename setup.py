from setuptools import setup, find_packages

setup(
    name="ggallery",
    version="0.1.0",
    description="A tool to generate static HTML photo galleries from various data sources.",
    author="Radzivon Chorny",
    author_email="mityy2012@gmail.com",
    packages=find_packages(),
    include_package_data=True,  # Include non-Python files (e.g., templates)
    install_requires=[
        "azure-storage-blob==12.24.1",
        "Pillow==11.1.0",
        "Jinja2==3.1.5",
        "PyYAML==6.0.2",
        "python-dotenv==1.0.1",
    ],
    entry_points={
        "console_scripts": [
            "ggallery=ggallery.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)