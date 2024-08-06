"""Module with behavior tree services."""

# Init/de-init
# maybe recommend to have waitt for trigger at end of eacha ction.
# wait for behaviortree_stop , data: unique id

# resturing status from running action
# maybe use events behaviortree_status, data: UID + status


from __future__ import annotations

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
)

from homeassistant.helpers.script import Script

from .const import DOMAIN

CONF_ACTIONS: Final = "actions"

SCHEMA_SERVICE_SEQUENCE = vol.Schema(
    {
        vol.Required(CONF_ACTIONS): vol.All(cv.ensure_list, cv.SCRIPT_SCHEMA),
    }
)

SERVICE_SEQUENCE: Final = "sequence"

SERVICES: Final = [
    SERVICE_SEQUENCE,
]

async def async_setup_services(hass: HomeAssistant) -> None:
    """Create the services."""

    async def async_service_sequence(service: ServiceCall) -> ServiceResponse:
        """A behavior tree sequence"""
        sequence = service.data.get(CONF_ACTIONS)
        script = Script(hass, sequence, "sequence", DOMAIN)
        result = await script.async_run(
            run_variables={},
            context=service.context,
        )
        if service.return_response:
            return result.service_response or {}
        return None

    hass.services.async_register(
        domain=DOMAIN,
        service=SERVICE_SEQUENCE,
        service_func=async_service_sequence,
        schema=SCHEMA_SERVICE_SEQUENCE,
        supports_response=SupportsResponse.OPTIONAL,
    )

async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload Homematic(IP) Local services."""
    for service in SERVICES:
        hass.services.async_remove(domain=DOMAIN, service=service)
