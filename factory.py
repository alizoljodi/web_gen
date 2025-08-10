from abc import ABC, abstractmethod
from typing import Dict, Type, Any

# Abstract base classes for models and views
class BaseModel(ABC):
    """Abstract base class for all models"""
    pass

class BaseView(ABC):
    """Abstract base class for all views"""
    pass

class BaseFactory(ABC):
    """Abstract base class for factories"""
    
    @abstractmethod
    def create(self, *args, **kwargs):
        pass

class ModelFactory(BaseFactory):
    """Factory for creating model instances"""
    
    def __init__(self):
        self._models: Dict[str, Type[BaseModel]] = {}
        self._instances: Dict[str, BaseModel] = {}
    
    def register_model(self, name: str, model_class: Type[BaseModel]):
        """Register a model class with the factory"""
        self._models[name] = model_class
    
    def create(self, name: str, *args, **kwargs) -> BaseModel:
        """Create a model instance by name"""
        if name not in self._models:
            raise ValueError(f"Model '{name}' not registered in factory")
        
        # For models that should be singletons, return existing instance
        if name in self._instances:
            return self._instances[name]
        
        # Create new instance
        instance = self._models[name](*args, **kwargs)
        
        # Store instance for potential reuse
        self._instances[name] = instance
        
        return instance
    
    def get_registered_models(self) -> list:
        """Get list of registered model names"""
        return list(self._models.keys())

class ViewFactory(BaseFactory):
    """Factory for creating view instances"""
    
    def __init__(self):
        self._views: Dict[str, Type[BaseView]] = {}
        self._instances: Dict[str, BaseView] = {}
    
    def register_view(self, name: str, view_class: Type[BaseView]):
        """Register a view class with the factory"""
        self._views[name] = view_class
    
    def create(self, name: str, *args, **kwargs) -> BaseView:
        """Create a view instance by name"""
        if name not in self._views:
            raise ValueError(f"View '{name}' not registered in factory")
        
        # For views that should be singletons, return existing instance
        if name in self._instances:
            return self._instances[name]
        
        # Create new instance
        instance = self._views[name](*args, **kwargs)
        
        # Store instance for potential reuse
        self._instances[name] = instance
        
        return instance
    
    def get_registered_views(self) -> list:
        """Get list of registered view names"""
        return list(self._views.keys())

class AppFactory:
    """Main factory that coordinates model and view factories"""
    
    def __init__(self):
        self.model_factory = ModelFactory()
        self.view_factory = ViewFactory()
        self._register_default_components()
    
    def _register_default_components(self):
        """Register default models and views"""
        # Import here to avoid circular imports
        from models import Message, ChatSession, HTMLGenerator, FileManager
        from views import CSSStyles, ChatView, ResultsView, PublishedView, FooterView
        
        # Register models
        self.model_factory.register_model("Message", Message)
        self.model_factory.register_model("ChatSession", ChatSession)
        self.model_factory.register_model("HTMLGenerator", HTMLGenerator)
        self.model_factory.register_model("FileManager", FileManager)
        
        # Register views
        self.view_factory.register_view("CSSStyles", CSSStyles)
        self.view_factory.register_view("ChatView", ChatView)
        self.view_factory.register_view("ResultsView", ResultsView)
        self.view_factory.register_view("PublishedView", PublishedView)
        self.view_factory.register_view("FooterView", FooterView)
    
    def create_model(self, name: str, *args, **kwargs) -> BaseModel:
        """Create a model instance"""
        return self.model_factory.create(name, *args, **kwargs)
    
    def create_view(self, name: str, *args, **kwargs) -> BaseView:
        """Create a view instance"""
        return self.view_factory.create(name, *args, **kwargs)
    
    def register_custom_model(self, name: str, model_class: Type[BaseModel]):
        """Register a custom model class"""
        self.model_factory.register_model(name, model_class)
    
    def register_custom_view(self, name: str, view_class: Type[BaseView]):
        """Register a custom view class"""
        self.view_factory.register_view(name, view_class)
    
    def get_available_models(self) -> list:
        """Get list of available model names"""
        return self.model_factory.get_registered_models()
    
    def get_available_views(self) -> list:
        """Get list of available view names"""
        return self.view_factory.get_registered_views()

# Global factory instance
app_factory = AppFactory()
