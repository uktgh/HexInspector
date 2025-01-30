from abc import ABC, abstractmethod

class PluginInterface(ABC):
    """
    Base class for all plugins. All plugins must inherit from this class and implement the required methods.
    """

    @abstractmethod
    def initialize(self, config):
        """
        Initialize the plugin with the given configuration.
        
        :param config: A dictionary containing configuration parameters for the plugin.
        """
        pass

    @abstractmethod
    def execute(self, data):
        """
        Execute the plugin's main functionality.
        
        :param data: The data to be processed by the plugin.
        :return: The result of the plugin's processing.
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        Perform any cleanup necessary when the plugin is being shut down.
        """
        pass

class PluginManager:
    """
    Manages the registration and execution of plugins.
    """

    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin):
        """
        Register a new plugin.
        
        :param plugin: An instance of a class that inherits from PluginInterface.
        """
        if not isinstance(plugin, PluginInterface):
            raise TypeError("Plugin must be an instance of PluginInterface")
        self.plugins.append(plugin)

    def initialize_plugins(self, config):
        """
        Initialize all registered plugins with the given configuration.
        
        :param config: A dictionary containing configuration parameters for all plugins.
        """
        for plugin in self.plugins:
            plugin.initialize(config)

    def execute_plugins(self, data):
        """
        Execute all registered plugins with the given data.
        
        :param data: The data to be processed by the plugins.
        :return: A list of results from each plugin.
        """
        results = []
        for plugin in self.plugins:
            result = plugin.execute(data)
            results.append(result)
        return results

    def shutdown_plugins(self):
        """
        Shutdown all registered plugins.
        """
        for plugin in self.plugins:
            plugin.shutdown()
