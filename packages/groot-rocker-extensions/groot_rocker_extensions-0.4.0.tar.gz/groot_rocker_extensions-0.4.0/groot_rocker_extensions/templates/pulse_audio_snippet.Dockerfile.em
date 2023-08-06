
@[if user_active ]@
USER root
@[end if]@

RUN DEBIAN__FRONTEND=noninteractive apt-get update && apt-get install -y --no-install-recommends @(audio_dependencies)    

RUN mkdir -p /etc/pulse

RUN echo '\n\
# Connect to the hosts server using the mounted UNIX socket\n\
default-server = unix:@(pulse_socket)\n\
\n\
# Prevent a server running in the container\n\
autospawn = no\n\
daemon-binary = /bin/true\n\
\n\
# Prevent the use of shared memory\n\
enable-shm = false\n\
\n'\
> /etc/pulse/client.conf

@[if user_active ]@
USER @(user_name)
@[end if]@
