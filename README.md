# Custom_component for [ha-dockermon](https://github.com/philhawthorne/ha-dockermon)
![Version](https://img.shields.io/badge/version-2.0.0-green.svg?style=for-the-badge) ![mantained](https://img.shields.io/maintenance/yes/2018.svg?style=for-the-badge)   
A custom platform which allows you to interact with [ha-dockermon.](https://github.com/philhawthorne/ha-dockermon)
  
To get started put `/custom_components/switch/hadockermon.py` here:
`<config directory>/custom_components/switch/hadockermon.py`  
  
**Example configuration.yaml:**
```yaml
switch:
  platform: hadockermon
  host: 192.168.1.50
  port: 8126
  stats: true
  exclude:
```
**Configuration variables:**  
  
key | description  
:--- | :---  
**platform (Required)** | The platform name.  
**host (Required)** | The IP address of your Docker host.  
**port (Optional)** | The port that the service is exposed on.  
**stats (Optional)** | Show memory and network usage of the containers, this does _not_ work on every docker host.  
**exclude (Optional)** | A list of Docker containers you want to exclude.  
  
[Home-Assistant demo site.](https://ha-test-hadcokermon.halfdecent.io/)
  
To start using this make sure you have [ha-dockermon](https://github.com/philhawthorne/ha-dockermon) running.  
