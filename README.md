# Google Nest Fan 


[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square&logo=homeassistantcommunitystore)](https://hacs.xyz/)
![GitHub Release](https://img.shields.io/github/v/release/iluvdata/google_nest_fan)
![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Filuvdata%2Fgoogle_nest_fan%2Frefs%2Ftags%2F2025.7.1%2Fcustom_components%2Ftplink_cloud%2Fmanifest.json&query=%24.version&prefix=v&label=dev-version)


A custom HomeAssistant integration that creates two additional entities for each Google Device with a Fan "trait" such as a Nest Thermostat.  These entities will allow you to set the fan to run for a customized amount of time (rather than the 12 hours hard coded into the core [Google Nest](https://www.home-assistant.io/integrations/nest/) integration.  The core Google Nest Integration must be configured and working for this integration to work.

## Installation with HACS

The recommended way to install this is via HACS:



[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=custom_respository&owner=iluvdata&repository=google_nest_fan)

#### Semi-manual install

1. Click on HACS in the Homeassistant side bar
2. Click on the three dots in the upper right-hand corner and select "Custom repositories."
3. In the form enter:

    1. Respository: `iluvdata/google_nest_fan`
    2. Select "Integration" as "Type"

## Manual Installation

Copy the `google_nest_fan` directory to the `custom_components` directory of your Homeassistant Instance.

## Configuration


Add the intergration to Home Assistant:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=google_nest_fan)

If the core **Google Nest** integration is configured this integration should be able to discover your devices with fan and add the additional controls.

## Use

Simple use the slider to select the amount of time you want to run the fan.  Upon changing the slider, it should send the request to the device to start the fan for the given duration.  To stop the fan, simply turn off through the core integration.   If you update the slider, it should change the duration to the most recent selected value.

