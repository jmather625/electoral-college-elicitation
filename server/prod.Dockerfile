FROM tiangolo/meinheld-gunicorn-flask:python3.7

# Clone code
RUN mkdir -p /build
RUN mkdir -p /logs
RUN git clone https://github.com/jmather625/electoral-college-elicitation /build/electoral-college-elicitation
RUN cd /build/electoral-college-elicitation && git pull
RUN cp -r /build/electoral-college-elicitation/server/* /app
RUN cp /build/electoral-college-elicitation/*.py /app
RUN cp /build/electoral-college-elicitation/*.pkl /app

# Install dependencies
RUN pip install -r /build/electoral-college-elicitation/requirements.txt

# Make port 80 available for links and/or publish
EXPOSE 80
