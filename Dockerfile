# Build stage: compile Python dependencies
FROM python:3.9-alpine as builder
RUN apk update
RUN apk add alpine-sdk
RUN python3 -m pip install --upgrade pip
COPY requirements.txt ./
RUN python3 -m pip install --user -r requirements.txt
# Install dotenv dependency
RUN python3 -m pip install python-dotenv


# Final stage: copy over Python dependencies and install production Node dependencies
FROM node:12-alpine
# this python version should match the build stage python version
RUN apk add python3
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local:$PATH
ENV NODE_ENV=production
# Uncomment the following line to enable agent logging
LABEL "network.forta.settings.agent-logs.enable"="true"
WORKDIR /app
COPY ./src ./src
COPY package*.json ./
COPY LICENSE.md ./

COPY secrets.json ./
COPY next_hour_file.json ./
COPY next_token_file.json ./
COPY combined_file.csv ./  
COPY deployer_addresses_unique.csv ./
COPY deployer_addresses.csv ./
COPY end_process_unique.csv ./
COPY end_process.csv ./
COPY result_data.csv ./
COPY sorted_deployer_addresses_unique.csv ./
COPY tweets_unique.csv ./
COPY tweets.csv ./
COPY result_urls.csv ./
COPY combined_urls.csv ./


RUN npm ci --production
CMD [ "npm", "run", "start:prod" ]


