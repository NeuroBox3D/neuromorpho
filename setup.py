import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='neuromorpho',
     version='0.0.1-a0',
     scripts=['neuromorpho'] ,
     author="Stephan Grein",
     author_email="stephan@syntaktischer-zucker.de",
     description="Query NeuroMorpho.org database via REST",
     long_description="This PyPi project allows users to query the NeuroMorpho.org database via REST request conveniently from the command line with Python2 or Python3 and integrates thus readily into a batch workflow. Database can be queried for cell names and neurons are downloaded in the SWC format.",
     long_description_content_type="text/markdown",
     url="https://github.com/stephanmg/neuromorpho",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
