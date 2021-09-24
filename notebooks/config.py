import yaml

with open("analysis_config.yml", mode="r") as fptr:
    analysis_config = yaml.safe_load(fptr)

analysis_config['all_variables'] = analysis_config['variables']['physics'] + analysis_config['variables']['biogeochemistry']
analysis_config['all_cases'] = [analysis_config['reference_case_name']] + analysis_config['compare_case_name'] 