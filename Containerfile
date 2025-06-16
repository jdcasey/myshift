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

FROM registry.fedoraproject.org/fedora-minimal:41

# Install Python and build dependencies
RUN microdnf -y update && \
    microdnf -y install \
    python3 \
    python3-pip \
    python3-devel \
    python3-build \
    python3-wheel \
    && microdnf clean all

# Create and set working directory
WORKDIR /app

# Copy the entire project
COPY . .

# Install the project and its dependencies
RUN pip install --no-cache-dir .

# Set the entrypoint
ENTRYPOINT ["/bin/bash"]
# ENTRYPOINT ["myshift"]

# # Default command (can be overridden)
# CMD ["repl"] 