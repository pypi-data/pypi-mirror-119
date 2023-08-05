#!/usr/bin/python3

#     Copyright 2021. FastyBird s.r.o.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""
Entities cache to prevent database overloading
"""

# Library dependencies
import datetime
import uuid
from abc import ABC
from typing import List
from modules_metadata.triggers_module import TriggerConditionOperator
from modules_metadata.types import SwitchPayload


class TriggerItem:
    """
    Trigger entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __trigger_id: uuid.UUID
    __enabled: bool

    # -----------------------------------------------------------------------------

    def __init__(self, trigger_id: uuid.UUID, enabled: bool) -> None:
        self.__trigger_id = trigger_id
        self.__enabled = enabled

    # -----------------------------------------------------------------------------

    @property
    def trigger_id(self) -> uuid.UUID:
        """Trigger identifier"""
        return self.__trigger_id

    # -----------------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """Flag informing if trigger is enabled"""
        return self.__enabled


class ConditionItem(ABC):
    """
    Base condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __condition_id: uuid.UUID
    __trigger_id: uuid.UUID
    __enabled: bool

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
    ) -> None:
        self.__condition_id = condition_id
        self.__trigger_id = trigger_id
        self.__enabled = enabled

    # -----------------------------------------------------------------------------

    @property
    def condition_id(self) -> uuid.UUID:
        """Condition identifier"""
        return self.__condition_id

    # -----------------------------------------------------------------------------

    @property
    def trigger_id(self) -> uuid.UUID:
        """Condition identifier"""
        return self.__trigger_id

    # -----------------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """Flag informing if condition is enabled"""
        return self.__enabled


class PropertyConditionItem(ConditionItem):
    """
    Base property condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __operator: TriggerConditionOperator
    __operand: str

    __device: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        operator: TriggerConditionOperator,
        operand: str,
        device: uuid.UUID,
    ) -> None:
        super().__init__(condition_id, trigger_id, enabled)

        self.__operator = operator
        self.__operand = operand

        self.__device = device

    # -----------------------------------------------------------------------------

    @property
    def device(self) -> uuid.UUID:
        """Device identifier"""
        return self.__device

    # -----------------------------------------------------------------------------

    @property
    def operator(self) -> TriggerConditionOperator:
        """Condition operator"""
        return self.__operator

    # -----------------------------------------------------------------------------

    @property
    def operand(self) -> str:
        """Condition operand"""
        return self.__operand

    # -----------------------------------------------------------------------------

    def validate(
        self,
        previous_value: str or None,
        actual_value: str
    ) -> bool:
        """Property value validation"""
        if previous_value is not None and previous_value == actual_value:
            return False

        if self.__operator == TriggerConditionOperator.EQUAL:
            return self.operand == actual_value

        if self.__operator == TriggerConditionOperator.ABOVE:
            return self.operand < actual_value

        if self.__operator == TriggerConditionOperator.BELOW:
            return self.operand > actual_value

        return False


class DevicePropertyConditionItem(PropertyConditionItem):
    """
    Device property condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __device_property: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        operator: TriggerConditionOperator,
        operand: str,
        device_property: uuid.UUID,
        device: uuid.UUID,
    ) -> None:
        super().__init__(condition_id, trigger_id, enabled, operator, operand, device)

        self.__device_property = device_property

    # -----------------------------------------------------------------------------

    @property
    def device_property(self) -> uuid.UUID:
        """Device property identifier"""
        return self.__device_property


class ChannelPropertyConditionItem(PropertyConditionItem):
    """
    Channel property condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __channel_property: uuid.UUID
    __channel: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        operator: TriggerConditionOperator,
        operand: str,
        channel_property: uuid.UUID,
        channel: uuid.UUID,
        device: uuid.UUID,
    ) -> None:
        super().__init__(condition_id, trigger_id, enabled, operator, operand, device)

        self.__channel_property = channel_property
        self.__channel = channel

    # -----------------------------------------------------------------------------

    @property
    def channel(self) -> uuid.UUID:
        """Channel identifier"""
        return self.__channel

    # -----------------------------------------------------------------------------

    @property
    def channel_property(self) -> uuid.UUID:
        """Channel property identifier"""
        return self.__channel_property


class TimeConditionItem(ConditionItem):
    """
    Time condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __time: datetime.timedelta
    __days: List[int]

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        time: datetime.timedelta,
        days: str,
    ) -> None:
        super().__init__(condition_id, trigger_id, enabled)

        self.__time = time
        self.__days = [int(x) for x in days.split(",")]

    # -----------------------------------------------------------------------------

    @property
    def time(self) -> datetime.timedelta:
        """Condition time"""
        return self.__time

    # -----------------------------------------------------------------------------

    @property
    def days(self) -> List[int]:
        """Condition days"""
        return self.__days


class DateConditionItem(ConditionItem):
    """
    Date condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __date: datetime.datetime

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        date: datetime.datetime,
    ) -> None:
        super().__init__(condition_id, trigger_id, enabled)

        self.__date = date

    # -----------------------------------------------------------------------------

    @property
    def date(self) -> datetime.datetime:
        """Condition date"""
        return self.__date


class PropertyActionItem(ABC):
    """
    Base property action entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __action_id: uuid.UUID
    __trigger_id: uuid.UUID
    __enabled: bool

    __value: str

    __device: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        action_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        value: str,
        device: uuid.UUID,
    ) -> None:
        self.__action_id = action_id
        self.__trigger_id = trigger_id
        self.__enabled = enabled

        self.__value = value

        self.__device = device

    # -----------------------------------------------------------------------------

    @property
    def device(self) -> uuid.UUID:
        """Device identifier"""
        return self.__device

    # -----------------------------------------------------------------------------

    @property
    def action_id(self) -> uuid.UUID:
        """Action identifier"""
        return self.__action_id

    # -----------------------------------------------------------------------------

    @property
    def trigger_id(self) -> uuid.UUID:
        """Action trigger identifier"""
        return self.__trigger_id

    # -----------------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """Flag informing if action is enabled"""
        return self.__enabled

    # -----------------------------------------------------------------------------

    @property
    def value(self) -> str:
        """Action property value to be set"""
        return self.__value

    # -----------------------------------------------------------------------------

    def validate(
        self,
        actual_value: str
    ) -> bool:
        """Property value validation"""
        if self.__value == SwitchPayload(SwitchPayload.TOGGLE).value:
            return False

        return self.__value == actual_value


class DevicePropertyActionItem(PropertyActionItem):
    """
    Device property action entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __device_property: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        action_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        value: str,
        device_property: uuid.UUID,
        device: uuid.UUID,
    ) -> None:
        super().__init__(action_id, trigger_id, enabled, value, device)

        self.__device_property = device_property

    # -----------------------------------------------------------------------------

    @property
    def device_property(self) -> uuid.UUID:
        """Device property identifier"""
        return self.__device_property


class ChannelPropertyActionItem(PropertyActionItem):
    """
    Channel property action entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """
    __channel_property: uuid.UUID
    __channel: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        action_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        value: str,
        channel_property: uuid.UUID,
        channel: uuid.UUID,
        device: uuid.UUID,
    ) -> None:
        super().__init__(action_id, trigger_id, enabled, value, device)

        self.__channel_property = channel_property
        self.__channel = channel

    # -----------------------------------------------------------------------------

    @property
    def channel(self) -> uuid.UUID:
        """Channel identifier"""
        return self.__channel

    # -----------------------------------------------------------------------------

    @property
    def channel_property(self) -> uuid.UUID:
        """Channel property identifier"""
        return self.__channel_property
