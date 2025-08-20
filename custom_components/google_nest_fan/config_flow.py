"""Config flow for the TPLink Cloud integration."""

from __future__ import annotations

import logging
from typing import Any

from google_nest_sdm.device import Device

# pylint: disable=hass-component-root-import
from homeassistant.components.nest.climate import ThermostatHvacTrait
from homeassistant.components.nest.const import DOMAIN as NEST_DOMAIN
from homeassistant.components.nest.types import NestConfigEntry

# pylint: enable=hass-component-root-import
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class GoogleNestFanFlow(ConfigFlow, domain=DOMAIN):
    """Google Nest Fan Flow."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Add the integration."""
        error: str = ""
        entries: list[NestConfigEntry] = self.hass.config_entries.async_loaded_entries(
            NEST_DOMAIN
        )
        if not entries:
            error = "nest_not_loaded"
        else:
            devices: list[Device] = []
            for entry in entries:
                devices.extend(
                    device
                    for device in entry.runtime_data.device_manager.devices.values()
                    if ThermostatHvacTrait.NAME in device.traits
                )
            if not devices:
                error = "no_thermostats"
        if not error:
            return self.async_create_entry(
                title="Google Nest Fan Customization",
                description="Will create entries for all Nest fans",
                data={},
            )
        return self.async_abort(reason=error)
