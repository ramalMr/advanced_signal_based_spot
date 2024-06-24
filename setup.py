from setuptools import setup, find_packages

setup(
    name='tech_sphere_tasks',
    version='1.0.0',
    description='Binance məlumatlarının analizi',
    author='ramal',
    author_email='techsphere',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'pandas',
        'numpy',
        'scipy',
        'python-binance',
    ],
)
