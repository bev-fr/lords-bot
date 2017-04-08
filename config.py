import yaml


#Bot Configuration
configFile = open("config.yml", 'r') 
cfg = yaml.safe_load(configFile)

for section in cfg:
    token = str(cfg['apitoken'])
    log = str(cfg['log'])
    creator = int(cfg['creator-id'])
    log_channel = cfg['log_channel']
