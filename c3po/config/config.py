from configparser import ConfigParser


def read_config(filename="config.ini", section=""):
    if not section:
        raise Exception("Section not specified")

    parser = ConfigParser()
    parser.optionxform = str
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )
    return config
