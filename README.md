# Custom_component for [ha-dockermon](https://github.com/philhawthorne/ha-dockermon)
![Version](https://img.shields.io/badge/version-2.0.1-green.svg?style=for-the-badge)
  
A custom component which allows you to interact with [ha-dockermon.](https://github.com/philhawthorne/ha-dockermon)
  
To get started put `/custom_components/hadockermon.py` here:
`<config directory>/custom_components/hadockermon.py`  
  
**Example configuration.yaml:**
```yaml
hadockermon:
  exclude: 'NGINX', 'ha-dockermon'
  host: 192.168.1.50
  platform: hadockermon
  port: 8126
  stats: true
```
**Configuration variables::**  
**host (Required)**: null  
**platform (Required)**: null  
**exclude (Optional)**: null  
**port (Optional)**: null  
**stats (Optional)**: null  
#### Sample overview
![Sample overview](overview.png)
  
[Home-Assistant demo site.](https://ha-test-hadcokermon.halfdecent.io/)
  
To start using this make sure you have [ha-dockermon](https://github.com/philhawthorne/ha-dockermon) running.  
