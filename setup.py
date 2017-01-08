from setuptools import setup

setup(name='lutronqs',
        version='0.2',
        description='Implementation of the Lutron QS integration protocol.',
        long_description='Implementation and command line utility for interfacing with a subset of the integration features of Lutron QS lighting systems.',
        url='https://github.com/nkaminski/lutronqs',
        classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Home Automation',
        ],
        keywords='Lutron lighting automation HomeWorks Quantum',
        author='Nash Kaminski',
        author_email='nashkaminski@kaminski.io',
        license='LGPLv3',
        packages=['lutronqs'],
        install_requires=[],
        scripts=['bin/lutronqs-cli'],
        zip_safe=False)
