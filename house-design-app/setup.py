from setuptools import setup, find_packages

setup(
    name='house-design-app',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python application for modeling walls and designing houses in 2D and 3D.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your project dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)