FROM mongo

# workdir
WORKDIR /usr/src/configs

# install dependency
COPY replica.js .
COPY setup.sh .

RUN ["chmod", "+x", "/usr/local/bin/docker-entrypoint.sh"]
# command
CMD ["./setup.sh"]