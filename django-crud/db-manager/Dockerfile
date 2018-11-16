FROM mongo

# workdir
WORKDIR /usr/src/configs

# copy config files
COPY mongo.conf .

# define port
EXPOSE 27017

# command
CMD ["--config", "./mongo.conf"]