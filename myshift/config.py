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

import os
import sys
from typing import List, Dict, Any
import yaml
import platform

def get_config_locations() -> List[str]:
    system = platform.system()
    if system == 'Darwin':
        return [
            '/Library/Application Support/spre-config.yaml',
            os.path.expanduser('~/Library/Application Support/spre-config.yaml'),
            os.path.expanduser('~/.config/spre-config.yaml'),
            os.path.join(os.getcwd(), 'spre-config.yaml')
        ]
    else:
        return [
            '/etc/spre-config.yaml',
            os.path.expanduser('~/.config/spre-config.yaml'),
            os.path.join(os.getcwd(), 'spre-config.yaml')
        ]

def load_config() -> Dict[str, Any]:
    for path in get_config_locations():
        if os.path.exists(path):
            with open(path, 'r') as f:
                return yaml.safe_load(f)
    print('spre-config.yaml not found in standard locations.', file=sys.stderr)
    sys.exit(1) 