FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN python3 -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
COPY . /code/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
