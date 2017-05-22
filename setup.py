"""Setup for Echo Serr."""


from setuptools import setup


extra_packages = {
    'testing': ['ipython', 'pytest', 'pytest-watch', 'pytest-cov', 'tox']
}


setup(
    name='echo',
    desctription='Client sends a msg, receives it back, and then returns it.',
    version='0.1',
    author='Ophelia Yin, James Feore',
    author_email='yo@whatup.com, sup@dawg.com',
    license='MIT',
    py_modules=['client', 'server'],
    package_dir={'': 'src'},
    install_requires=[],
    extras_require=extra_packages,
    entry_points={
        'console_scripts': [
            'client = client:client'
        ]
    }
)
