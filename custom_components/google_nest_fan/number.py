"""Fan time select."""

from google_nest_sdm.device import Device
from google_nest_sdm.device_traits import FanTrait

from homeassistant.components.nest import ApiException

# pylint: disable-next=hass-component-root-import
from homeassistant.components.nest.device_info import NestDeviceInfo
from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberMode
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import GoogleNestFan


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GoogleNestFan,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Setup up the number entities for each Nest SDM Fan."""
    fan_run_time_entities: list[FanRunTime] = []
    for device in entry.runtime_data.devices:
        if FanTrait.NAME in device.traits:
            fan_trait = device.traits[FanTrait.NAME]
            if fan_trait.timer_mode is not None:
                fan_run_time_entities.append(FanRunTime(device))
    if fan_run_time_entities:
        async_add_entities(fan_run_time_entities)


class FanRunTime(NumberEntity):
    """Number of hours to run fan."""

    _attr_should_poll = False
    _attr_has_entity_name = True
    _attr_device_class = NumberDeviceClass.DURATION
    _attr_mode = NumberMode.SLIDER
    _attr_native_max_value = 15
    _attr_native_min_value = 0
    _attr_native_step = 0.25
    _attr_native_unit_of_measurement = UnitOfTime.HOURS
    _attr_native_value = 0
    _attr_icon = "mdi:fan-clock"
    _attr_name = "Run Fan"

    def __init__(self, device: Device) -> None:
        """Initialize."""
        self._device: Device = device
        self._device_info = NestDeviceInfo(device)
        # The API "name" field is a unique device identifier.
        self._attr_unique_id = f"{device.name}-{self.device_class}"
        self._attr_device_info = self._device_info.device_info

    async def async_set_native_value(self, value: float) -> None:
        """User updated the value."""
        if value == 0:
            return
        runtime: int = round(3600 * value)
        trait = self._device.traits[FanTrait.NAME]
        try:
            await trait.set_timer("ON", duration=runtime)
        except ApiException as err:
            raise HomeAssistantError(
                f"Error setting fan run time for {self.entity_id} {value} h: {err}"
            ) from err
        self._attr_native_value = 0
