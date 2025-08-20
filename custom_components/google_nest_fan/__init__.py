"""Setup Google Nest Fan Integration."""

from dataclasses import dataclass

from google_nest_sdm.device import Device

# pylint: disable=hass-component-root-import
from homeassistant.components.nest.climate import ThermostatHvacTrait
from homeassistant.components.nest.const import DOMAIN as NEST_DOMAIN
from homeassistant.components.nest.types import NestConfigEntry

# pylint: enable=hass-component-root-import
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError

from .const import DOMAIN, PLATFORMS


@dataclass
class GoogleNestFanData:
    """Class to hold integration data."""

    devices: list[Device]


type GoogleNestFan = ConfigEntry[GoogleNestFanData]


async def async_setup_entry(hass: HomeAssistant, entry: GoogleNestFan) -> bool:
    """Setup this config."""
    entries: list[NestConfigEntry] = hass.config_entries.async_loaded_entries(
        NEST_DOMAIN
    )
    if not entries:
        raise ConfigEntryError(
            translation_domain=DOMAIN, translation_key="nest_not_loaded"
        )
    devices: list[Device] = []
    for nestentry in entries:
        devices.extend(
            device
            for device in nestentry.runtime_data.device_manager.devices.values()
            if ThermostatHvacTrait.NAME in device.traits
        )
    if not devices:
        raise ConfigEntryError(
            translation_domain=DOMAIN, translation_key="no_thermostats"
        )
    entry.runtime_data = GoogleNestFanData(devices)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True
