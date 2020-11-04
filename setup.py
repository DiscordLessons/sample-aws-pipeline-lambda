import setuptools

setuptools.setup(
    name='python_lambda_function_brianw',
    version='1.1.1',
    author='Brian Wijaya',
    author_email='brianwijay14@gmail.com',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    description='Lambda Function with requests module installed for Python',
    packages=['python_function'],
    install_requires=[
          'requests',
      ],
    python_requires='>=3.6',
)
