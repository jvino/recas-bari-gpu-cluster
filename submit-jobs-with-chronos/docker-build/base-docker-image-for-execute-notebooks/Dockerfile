FROM registry-clustergpu.recas.ba.infn.it/gvino/jupyterhub-batch:v2

# Environment configuration
ENV USERNAME=<username>
ENV USERID=<user_uid>
ENV GROUPID=<user_gid>
ENV HOME=<user_home>
ENV USER_HOME=$HOME

# User creation
RUN groupadd \
        -g $GROUPID $USERNAME && \
    adduser \
        --disabled-password \ 
        --gecos '' \
        --uid $USERID \
        --gid $GROUPID $USERNAME \
        --home $HOME

# Enable user environment
USER $USERNAME
WORKDIR $USER_HOME