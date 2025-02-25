# Copyright 2018 Open Source Robotics Foundation, Inc.
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

"""Module for Shutdown event."""

from typing import Text

from ..event import Event


class Shutdown(Event):
    """Event that is emitted on shutdown of a launched system."""

    name = 'launch.events.Shutdown'

    def __init__(self, *, reason = 'reason not given', due_to_sigint = False):
        """Constructor."""
        self.__reason = reason
        self.__due_to_sigint = due_to_sigint

    @property
    def reason(self):
        """Getter for reason."""
        return self.__reason

    @property
    def due_to_sigint(self):
        """Getter for due_to_sigint."""
        return self.__due_to_sigint
