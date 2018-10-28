'''
A component which allows you to interact with ha-dockermon.

ha-dockermon: https://github.com/philhawthorne/ha-dockermon

For more details about this component, please refer to the documentation at
https://github.com/custom-components/switch.hadockermon
'''
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from time import sleep
from datetime import timedelta
from homeassistant.core import ServiceCall
from homeassistant.util import slugify
from homeassistant.components.switch import (SwitchDevice,
    PLATFORM_SCHEMA, ENTITY_ID_FORMAT)

__version__ = '2.1.0'

REQUIREMENTS = ['pydockermon==0.1.2']

CONF_HOST = 'host'
CONF_PORT = 'port'
CONF_USERNAME = 'username'
CONF_PASSWORD = 'password'
CONF_STATS = 'stats'
CONF_PREFIX = 'prefix'
CONF_INCLUDE = 'include'

ATTR_STATUS = 'status'
ATTR_IMAGE = 'image'
ATTR_MEMORY = 'memory'
ATTR_RX_TOTAL = 'network_rx_total'
ATTR_TX_TOTAL = 'network_tx_total'
ATTR_FRIENDLY_NAME = 'friendly_name'

SCAN_INTERVAL = timedelta(seconds=60)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default='8126'): cv.string,
    vol.Optional(CONF_USERNAME, default=''): cv.string,
    vol.Optional(CONF_PASSWORD, default=''): cv.string,
    vol.Optional(CONF_STATS, default='False'): cv.string,
    vol.Optional(CONF_PREFIX, default='None'): cv.string,
    vol.Optional(CONF_INCLUDE, default=None): 
        vol.All(cv.ensure_list, [cv.string]),
})

def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    import pydockermon
    dm = pydockermon
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    include = config.get(CONF_INCLUDE)
    stats = config.get(CONF_STATS)
    prefix = config.get(CONF_PREFIX)
    dev = []
    containers = dm.list_containers(host, port, username, password)

    if containers:
        for container in containers['data']:
            if container in include or include is None:
                dev.append(ContainerSwitch(container,
                    stats, host, port, username, password, dm, prefix))
        add_devices_callback(dev, True)
    else:
        return False

class ContainerSwitch(SwitchDevice):
    def __init__(self, name, stats, host, port, username, password, dm, prefix):
        _slow_reported = True
        if prefix == 'None':
            self.entity_id = ENTITY_ID_FORMAT.format(slugify(name))
        else:
            self.entity_id = ENTITY_ID_FORMAT.format(slugify(prefix + '_' + name))
        self._dm = dm
        self._state = False
        self._name = name
        self._stats = stats
        self._network_stats = None
        self._status = None
        self._image = None
        self._memory_usage = None
        self._network_rx_total = None
        self._network_tx_total = None
        self._host = host
        self._port = port
        self._username = username
        self._password = password

    def update(self):
        containerstate = self._dm.get_container_state(self._name,
            self._host, self._port, self._username, self._password)
        if not containerstate['success']:
            self._state = False
        else:
            data = containerstate['data']
            state = data['state']
            self._status = data['status']
            self._image = data['image']
            if state == 'running':
                if self._stats == 'True':
                    containerstats = self._dm.get_container_stats(self._name,
                        self._host, self._port, self._username, self._password)
                    if not containerstats['success']:
                        return False
                    else:
                        data = containerstats['data']
                        get_memory = data['memory_stats']
                        memory_usage = get_memory['usage']/1024/1024
                        try:
                            data['networks']
                        except Exception:
                            self._network_rx_total = None
                            self._network_tx_total = None
                        else:
                            self._network_stats = 'aviable'
                            netstats = data['networks']['eth0']
                            network_rx_total = netstats['rx_bytes']/1024/1024
                            network_tx_total = netstats['tx_bytes']/1024/1024
                            self._network_rx_total = str(round(
                                network_rx_total, 2)) + ' MB'
                            self._network_tx_total = str(round(
                                network_tx_total, 2)) + ' MB'
                        self._memory_usage = str(round(
                            memory_usage, 2)) + ' MB'
                self._state = True
            else:
                self._state = False

    @property
    def should_poll(self):
        return True

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return 'mdi:docker'

    @property
    def device_state_attributes(self):
        if self._network_stats == 'aviable':
            return {
                ATTR_STATUS: self._status,
                ATTR_IMAGE: self._image,
                ATTR_MEMORY: self._memory_usage,
                ATTR_RX_TOTAL: self._network_rx_total,
                ATTR_TX_TOTAL: self._network_tx_total
            }
        elif self._stats == 'True':
            return {
                ATTR_STATUS: self._status,
                ATTR_IMAGE: self._image,
                ATTR_MEMORY: self._memory_usage
            }
        else: 
            return {
                ATTR_STATUS: self._status,
                ATTR_IMAGE: self._image
            }
            
    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        if self._name.startswith("addon_"):
            addon = self._name.replace("addon_", "")
            self.hass.bus.async_fire(event_type='call_service', 
                event_data={'domain': 'hassio','service': 'addon_start',
                    'service_data': {'addon': addon}})
        else:
            command = self._dm.start_container(self._name, self._host, self._port, self._username, self._password)
            if command == False:
                _LOGGER.error('Container failed to start.')
            else:
                self._state = False

        self._state = True
        sleep(5)
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        if self._name.startswith("addon_"):
            addon = self._name.replace("addon_", "")
            self.hass.bus.async_fire(event_type='call_service', 
                event_data={'domain': 'hassio','service': 'addon_stop',
                    'service_data': {'addon': addon}})
            self._state = False
        else:
            command = self._dm.stop_container(self._name, self._host, self._port, self._username, self._password)
            if command == False:
                _LOGGER.error('Container failed to turn off.')
            else:
                self._state = False
        sleep(5)
        self.schedule_update_ha_state()
