# layer 1: use the base image
FROM python:alpine

# layer 2: create and use a work directory
WORKDIR /vinod/app

# layer 3: copy requirements.txt
COPY ./requirements.txt .

# layer 4: install deps
RUN pip install -r requirements.txt

# layer 5: copy all other files (main.py)
COPY ./main.py .

# add the executable command
CMD ["python3", "main.py"]



