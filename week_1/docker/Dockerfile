FROM python:3.9.1

RUN pip3 install pandas

#change the working directory - it's like cd command in linux
WORKDIR /app  

# copy the file from current folder in the host machine to the working directory
COPY pipeline.py pipeline.py 

# run the python pipeline.py command when we use docker run command
ENTRYPOINT [ "python3", "pipeline.py" ] 