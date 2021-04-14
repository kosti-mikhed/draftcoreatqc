import setuptools


with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name='draft_core_atqc',
    version='0.0.3',
    description='Draft framework core',
    long_description=readme,
    url='git@github.com:kosti-mikhed/draft-core-atqc.git',
    author='Kosti Mikhed',
    author_email='kosti.mikhed@teck.com',
    license='unlicense',
    packages=['draft-core-atqc'],
    include_package_data=True
)
