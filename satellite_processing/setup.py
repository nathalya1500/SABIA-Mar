from setuptools import setup, find_packages

setup(
    name="satellite_processing",
    version="1.0.0",
    author="Facundo Godoy",
    description="Un paquete para el procesamiento de imagenes satelitales de L2 a L3 bineadas",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "h5py",
        "tqdm",
    ],
)
