# switch.hadockermon [![Build Status](https://travis-ci.com/custom-components/switch.hadockermon.svg?branch=master)](https://travis-ci.com/custom-components/switch.hadockermon)

_Custom_component for [ha-dockermon.][hadockermon]_

A custom platform which allows you to interact with [ha-dockermon.][hadockermon]
  
To get started put [`switch.py`](https://raw.githubusercontent.com/custom-components/switch.hadockermon/master/custom_components/hadockermon/switch.py), [`__init__.py`](https://raw.githubusercontent.com/custom-components/switch.hadockermon/master/custom_components/hadockermon/__init__.py) and [`manifest.json`](https://raw.githubusercontent.com/custom-components/switch.hadockermon/master/custom_components/hadockermon/manifest.json) from [`/custom_components/hadockermon/`](/custom_components/hadockermon) here:  
`<config directory>/custom_components/hadockermon/switch.py`  	`<config directory>/custom_components/hadockermon/`
  
**Example configuration.yaml:**

```yaml
switch:
  platform: hadockermon
  host: 192.168.1.50
  port: 8126
  containers:
    - 'NGINX'
    - 'ha-dockermon'
```

**Configuration variables:**  
  
key | description  
:--- | :---  
**platform (Required)** | The platform name.  
**host (Required)** | The IP address of your Docker host running ha-dockermon.  
**port (Optional)** | The port that the service is exposed on.  
**containers (Optional)** | A list of containers you want to control, by default it shows all.
  
## Sample overview

![Sample overview](example.png)

**To start using this make sure you have [ha-dockermon][hadockermon] running.**  

***
Due to how `custom_components` are loaded, it is normal to see a `ModuleNotFoundError` error on first boot after adding this, to resolve it, restart Home-Assistant.
***

[buymeacoffee.com][buymeacoffee]

<!-- Links -->
[buymeacoffee]: https://www.buymeacoffee.com/ludeeus
[hadockermon]: https://github.com/philhawthorne/ha-dockermon
