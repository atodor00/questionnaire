import yaml

def read_config(file_path):
    """
    Reads a YAML configuration file and returns its contents.

    :param file_path: Path to the configuration file
    :return: Parsed YAML data as a dictionary
    """
    try:
        with open(file_path, 'r') as file:
            config_data = yaml.safe_load(file)
        return config_data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except yaml.YAMLError:
        print(f"Error: The file {file_path} is not a valid YAML file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
if __name__ == "__main__":
    config_path = "../config/questionnaire.yaml"  # Replace with your actual file path
    config = read_config(config_path)

    if config:
        print("Configuration Loaded:")
        print(config['questionnaire']['title'])
        print(config['questionnaire']['description'] )
        # print(config['questionnaire']['questions'][0] )
        # print(config['questionnaire']['questions'][0]['id'] )
        # print(config['questionnaire']['questions'][0]['question'] )
        # print(config['questionnaire']['questions'][0]['type'] )
        for item in config['questionnaire']['questions']:
            print('')
            # print(str(item['id']) )
            print(str(item['question']) )
            if(item['type']) == "multiple_choice":
                # print(str(item['type']) )
                for option in item['options']:
                    print(str(option) )