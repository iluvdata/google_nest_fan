"""Show the timestamp when the fan will stop."""

import datetime
import logging

from google_nest_sdm.device import Device
from google_nest_sdm.device_traits import FanTrait

# pylint: disable-next=hass-component-root-import
from homeassistant.components.nest.device_info import NestDeviceInfo
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import GoogleNestFan

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GoogleNestFan,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Setup up the number entities for each Nest SDM Fan."""
    fan_run_stop_entities: list[FanStop] = []
    for device in entry.runtime_data.devices:
        if FanTrait.NAME in device.traits:
            fan_trait = device.traits[FanTrait.NAME]
            if fan_trait.timer_mode is not None:
                fan_run_stop_entities.append(FanStop(device))
    if fan_run_stop_entities:
        async_add_entities(fan_run_stop_entities)


class FanStop(SensorEntity):
    """Sensor to include fan stop time."""

    _attr_should_poll = False
    _attr_name = "Fan End Time"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:fan-clock"
    _attr_has_entity_name = True

    def __init__(self, device: Device) -> None:
        """Initialize the sensor."""
        super().__init__()
        self._device: Device = device
        self._device_info = NestDeviceInfo(device)
        # The API "name" field is a unique device identifier.
        self._attr_unique_id = f"{device.name}-{self.device_class}"
        self._attr_device_info = self._device_info.device_info

    @property
    def available(self) -> bool:  # pyright: ignore[reportIncompatibleVariableOverride]
        """Return device availability."""
        return self._device_info.available

    async def async_added_to_hass(self) -> None:
        """Run when entity is added to register update signal handler."""
        self.async_on_remove(
            self._device.add_update_listener(self.async_write_ha_state)
        )

    @property
    def native_value(self) -> datetime.datetime | str:  # pyright: ignore[reportIncompatibleVariableOverride]
        """Return the state of the sensor."""
        fan_trait: FanTrait = self._device.traits[FanTrait.NAME]
        _LOGGER.debug(
            "Updating fan timer timeout: %s, timerMode: %s",
            fan_trait.timer_timeout,
            fan_trait.timer_mode,
        )
        if not fan_trait.timer_timeout or fan_trait.timer_mode == "OFF":
            self._attr_device_class = None
            return "Not Running"
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        return fan_trait.timer_timeout
