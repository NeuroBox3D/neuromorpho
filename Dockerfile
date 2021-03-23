FROM python:3.8

WORKDIR /code

COPY externals /code/externals
COPY geometry_tools /code/geometry_tools
COPY rest_wrapper /code/rest_wrapper
COPY get_swc.py /code

ENTRYPOINT ["python", "/code/get_swc.py"]
