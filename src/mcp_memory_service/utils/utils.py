# Copyright 2024 Heinrich Krupp
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

from datetime import datetime
import logging

logger = logging.getLogger(__name__)  # Add this if not already at top of your file

def ensure_datetime(ts):
    """
    Ensure the input is a datetime object.

    - If ts is a datetime, return as is.
    - If ts is a float or int, assume it's a Unix timestamp and convert.
    - If ts is a string, try to parse as ISO format.
    - If ts is None, return None.
    Logs a warning if parsing fails.
    """
    if ts is None:
        return None
    if isinstance(ts, datetime):
        return ts
    if isinstance(ts, (float, int)):
        try:
            return datetime.fromtimestamp(ts)
        except Exception as e:
            logger.warning(f"Failed to convert timestamp {ts} to datetime from float/int: {e}")
            return None
    if isinstance(ts, str):
        try:
            return datetime.fromisoformat(ts)
        except ValueError as e:
            logger.warning(f"Failed to parse string timestamp '{ts}' as ISO datetime: {e}")
            return None
    logger.warning(f"Unsupported timestamp type: {type(ts)} with value: {ts}")
    return None