FROM python:3.8

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update \
    && apt-get install -y google-chrome-stable

# Set display port as an environment variable
ENV DISPLAY=:99

# cache the requirements
ADD requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the package
COPY JobReport/ JobReport/

# expose the dashboard port
EXPOSE 5050

# change workind directory
WORKDIR /JobReport

# command to run on container start 
ENTRYPOINT [ "python", "JobReport.py", "--container_env" ]