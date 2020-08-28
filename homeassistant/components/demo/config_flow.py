"""Config flow to configure demo component."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_ELEVATION, CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME

# pylint: disable=unused-import
from . import DOMAIN

CONF_STRING = "string"
CONF_BOOLEAN = "bool"
CONF_INT = "int"
CONF_SELECT = "select"
CONF_MULTISELECT = "multi"


class DemoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Demo configuration flow."""

    VERSION = 1

    def __init__(self):
        """Init FlowHandler."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            return self.async_create_entry(title="demo entry config", data=user_input)

        return await self._show_config_form(
            name="Demo",
            latitude=self.hass.config.latitude,
            longitude=self.hass.config.longitude,
            elevation=self.hass.config.elevation,
        )

    async def _show_config_form(
        self, name=None, latitude=None, longitude=None, elevation=None
    ):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default=name): str,
                    vol.Required(CONF_LATITUDE, default=latitude): cv.latitude,
                    vol.Required(CONF_LONGITUDE, default=longitude): cv.longitude,
                    vol.Required(CONF_ELEVATION, default=elevation): int,
                }
            ),
            errors=self._errors,
        )

    async def async_step_onboarding(self, data=None):
        """Handle a flow initialized by onboarding."""
        return self.async_create_entry(
            title="demo entry config", data={"onboarding": True}
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_import(self, import_info):
        """Set the config entry up from yaml."""
        return self.async_create_entry(title="demo entry config", data={"import": True})


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_options_1()

    async def async_step_options_1(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            self.options.update(user_input)
            return await self.async_step_options_2()

        return self.async_show_form(
            step_id="options_1",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_BOOLEAN,
                        default=self.config_entry.options.get(CONF_BOOLEAN, False),
                    ): bool,
                    vol.Optional(
                        CONF_INT, default=self.config_entry.options.get(CONF_INT, 10),
                    ): int,
                }
            ),
        )

    async def async_step_options_2(self, user_input=None):
        """Manage the options 2."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="options_2",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_STRING,
                        default=self.config_entry.options.get(CONF_STRING, "Default",),
                    ): str,
                    vol.Optional(
                        CONF_SELECT,
                        default=self.config_entry.options.get(CONF_SELECT, "default"),
                    ): vol.In(["default", "other"]),
                    vol.Optional(
                        CONF_MULTISELECT,
                        default=self.config_entry.options.get(
                            CONF_MULTISELECT, ["default"]
                        ),
                    ): cv.multi_select({"default": "Default", "other": "Other"}),
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(title="demo entry config", data=self.options)
