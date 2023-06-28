FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

RUN python3 -m venv /djvenv
ENV PATH="/djvenv/bin:$PATH"

WORKDIR /LinkUp

# Copy project files
COPY . /LinkUp/

# Install dependencies
RUN pip install -r /LinkUp/requirements.txt

# Expose ports
EXPOSE 8000

RUN chmod +x /LinkUp/start.sh
ENTRYPOINT ["/LinkUp/start.sh"]
