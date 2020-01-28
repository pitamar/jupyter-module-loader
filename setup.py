import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='jupyter-module-loader',
    version='0.0.1',
    author='Itamar Schen',
    author_email='itamarschen@gmail.com',
    description='A python package that allows importing Jupyter notebooks as python modules',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pitamar/jupyter-module-loader',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)


