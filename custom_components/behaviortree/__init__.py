"""Home Assistant custom component to provide behavior tree services"""

from .services import async_setup_services

async def async_setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""
    await async_setup_services(hass)
    return True
