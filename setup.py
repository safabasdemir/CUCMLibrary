from setuptools import setup, find_packages

setup(
    name='CUCMLib',
    version='0.1.0',
    author='SafaBasdemir',
    author_email='safabasdemir@gmail.com',
    description='CUCM ile etkileşim için bir kütüphane',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        'cucmlib': ['AXLAPI.wsdl', 'AXLEnums.xsd', 'AXLSoap.xsd'],
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
