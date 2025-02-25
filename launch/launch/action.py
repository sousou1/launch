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

"""Module for Action class."""

from typing import cast
from typing import List
from typing import Optional
from typing import Text

from .condition import Condition
from .launch_context import LaunchContext
from .launch_description_entity import LaunchDescriptionEntity

if False:
    from .frontend import Entity  # noqa: F401
    from .frontend import Parser  # noqa: F401


class Action(LaunchDescriptionEntity):
    """
    LaunchDescriptionEntity that represents a user intention to do something.

    The action describes the intention to do something, but also can be
    executed given a :class:`launch.LaunchContext` at runtime.
    """

    def __init__(self, *, condition = None):
        """
        Constructor.

        If the conditions argument is not None, the condition object will be
        evaluated while being visited and the action will only be executed if
        the condition evaluates to True.

        :param condition: Either a :py:class:`Condition` or None
        """
        self.__condition = condition

    @staticmethod
    def parse(entity, parser):
        """
        Return the `Action` action and kwargs for constructing it.

        This is only intended for code reuse.
        This class is not exposed with `expose_action`.
        """
        # Import here for avoiding cyclic imports.
        from .conditions import IfCondition
        from .conditions import UnlessCondition
        if_cond = entity.get_attr('if', optional=True)
        unless_cond = entity.get_attr('unless', optional=True)
        kwargs = {}
        if if_cond is not None and unless_cond is not None:
            raise RuntimeError("if and unless conditions can't be used simultaneously")
        if if_cond is not None:
            kwargs['condition'] = IfCondition(
                predicate_expression=parser.parse_substitution(if_cond)
            )
        if unless_cond is not None:
            kwargs['condition'] = UnlessCondition(
                predicate_expression=parser.parse_substitution(unless_cond)
            )
        return Action, kwargs

    @property
    def condition(self):
        """Getter for condition."""
        return self.__condition

    def describe(self):
        """Return a description of this Action."""
        return self.__repr__()

    def visit(self, context):
        """Override visit from LaunchDescriptionEntity so that it executes."""
        if self.__condition is None or self.__condition.evaluate(context):
            try:
                return cast(Optional[List[LaunchDescriptionEntity]], self.execute(context))
            finally:
                from .events import ExecutionComplete  # noqa
                event = ExecutionComplete(action=self)
                if context.would_handle_event(event):
                    future = self.get_asyncio_future()
                    if future is not None:
                        future.add_done_callback(
                            lambda _: context.emit_event_sync(event)
                        )
                    else:
                        context.emit_event_sync(event)
        return None

    def execute(self, context):
        """
        Execute the action.

        Should be overridden by derived class, but by default does nothing.
        """
        pass
