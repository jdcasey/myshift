# Copyright 2025 John Casey
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM registry.fedoraproject.org/fedora:41

# Install Python and build dependencies
RUN dnf -y update && \
    dnf -y install \
    python3.11 \
    python3.11-pip \
    python3.11-devel \
    gcc \
    && dnf clean all

# Set Python 3.11 as default
RUN alternatives --set python3 /usr/bin/python3.11

# Create and set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY myshift/ ./myshift/
COPY setup.py .

# Install the application
RUN pip3 install -e .

# Set the entrypoint
ENTRYPOINT ["myshift"]

# Default command (can be overridden)
CMD ["--help"] 