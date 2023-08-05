"""Packaging rewordapp."""

from setuptools import setup, find_packages


setup(
    name='rewordapp',
    version='0.0.2',
    license='BSD-3-Clause',
    license_files=['LICENSE'],
    description='The application to reword text.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tuyen Mathew Duong',
    author_email='tuyen@geekstrident.com',
    maintainer='Tuyen Mathew Duong',
    maintainer_email='tuyen@geekstrident.com',
    install_requires=[],
    url='https://github.com/Geeks-Trident-LLC/rewordapp',
    packages=find_packages(
        exclude=(
            'tests*', 'testing*', 'examples*',
            'build*', 'dist*', 'docs*', 'venv*'
        )
    ),
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'reword-app = rewordapp.application:execute',
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
