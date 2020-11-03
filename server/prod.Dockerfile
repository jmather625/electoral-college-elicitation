FROM tiangolo/meinheld-gunicorn-flask:python3.7

# Clone code
RUN mkdir -p /build
RUN mkdir -p /logs
RUN rm -rf /build/*
RUN git clone https://github.com/jmather625/electoral-college-elicitation /build/ee
RUN cd /build/ee && git checkout 369d8063a273fbc8e700e1445db1c78f729ba444
RUN cp -r /build/ee/server/* /app

# Install dependencies
RUN pip install -r /build/ee/requirements.txt

# Make port 80 available for links and/or publish
EXPOSE 80

# ADD loop.sh .
# RUN chmod +x loop.sh
# CMD ["bash", "-c", "./loop.sh"]

