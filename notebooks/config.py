import yaml

with open("analysis_config.yml", mode="r") as fptr:
    analysis_config = yaml.safe_load(fptr)