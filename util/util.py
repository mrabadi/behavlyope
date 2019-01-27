class Util(object):
    """
    Utility functions
    """

    @staticmethod
    def load_config(filename):
        config = {}
        with open(filename) as f:
            for line in f:
                parsed = line.strip().split(":")
                if parsed[0] != '':
                    config[parsed[0]] = parsed[1]
        return config

    @staticmethod
    def get_param(config, name, default):
        return config[name] if name in config else default

    @staticmethod
    def get_param_list(config, name, default):
        """
        TODO: This assumes always int in lists, which needs to be fixed.
        """
        if name not in config:
            return default
        param_list = []
        config_list = config[name].split(",")
        for config in config_list:
            param_list.append(int(config))
        return param_list
