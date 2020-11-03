FROM tiangolo/meinheld-gunicorn-flask:python3.7

# Clone code
RUN mkdir -p /build
RUN mkdir -p /logs
RUN rm -rf /build/*
RUN git clone https://github.com/jmather625/electoral-college-elicitation /build/electoral-college-elicitation
RUN cd /build/electoral-college-elicitation && git checkout 57688011426a0eea2d3865994e58e52892836cd5
RUN cp -r /build/electoral-college-elicitation/server/* /app

# Install dependencies
RUN pip install -r /build/electoral-college-elicitation/requirements.txt

# Make port 80 available for links and/or publish
EXPOSE 80

# ADD loop.sh .
# RUN chmod +x loop.sh
# CMD ["bash", "-c", "./loop.sh"]

