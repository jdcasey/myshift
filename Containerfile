# Use Fedora as the base image
FROM registry.fedoraproject.org/fedora:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install Python and pip
RUN dnf -y update && \
    dnf -y install python3 python3-pip && \
    dnf clean all

# Create a non-root user
RUN useradd -m -s /bin/bash myshift

# Create directory for configuration
RUN mkdir -p /etc/myshift && \
    chown -R myshift:myshift /etc/myshift

# Switch to non-root user
USER myshift

# Set working directory
WORKDIR /home/myshift

# Copy the project files
COPY --chown=myshift:myshift . /home/myshift/myshift/

# Install myshift in development mode
RUN cd /home/myshift/myshift && \
    pip3 install --user -e .

# Add myshift to PATH
ENV PATH="/home/myshift/.local/bin:${PATH}"

# Set the entry point to the myshift REPL
ENTRYPOINT ["myshift", "repl"]

# Document the volume mount point for configuration
VOLUME ["/etc/myshift/spre-config.yaml"] 