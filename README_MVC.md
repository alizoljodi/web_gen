# MVC Architecture Refactoring

This project has been refactored from a monolithic structure into a clean **Model-View-Controller (MVC)** architecture for better maintainability, testability, and code organization.

## Architecture Overview

### 🏗️ **Model Layer** (`models.py`)
Contains all data structures, business logic, and external API interactions.

**Classes:**
- **`Message`**: Represents individual chat messages with metadata
- **`ChatSession`**: Manages the overall chat session state
- **`HTMLGenerator`**: Handles AI-powered HTML generation using Groq API
- **`FileManager`**: Manages file operations (save, open, download)

**Responsibilities:**
- Data persistence and state management
- Business logic for HTML generation
- External API communication
- File system operations

### 🎨 **View Layer** (`views.py`)
Contains all UI components, styling, and presentation logic.

**Classes:**
- **`CSSStyles`**: Centralized CSS styling for different pages
- **`ChatView`**: Chat interface display components
- **`ResultsView`**: Results page display components
- **`PublishedView`**: Published website display components
- **`FooterView`**: Footer display component

**Responsibilities:**
- UI rendering and styling
- User interface components
- CSS management
- Presentation logic

### 🎮 **Controller Layer** (`controller.py`)
Coordinates between Model and View, handles application flow and user interactions.

**Classes:**
- **`AppController`**: Main application controller

**Responsibilities:**
- Application state management
- User interaction handling
- Navigation between different views
- Coordinating Model and View operations
- Streamlit session state synchronization

### 🚀 **Main Application** (`streamlit_app.py`)
Simple entry point that creates and runs the controller.

### 🏭 **Factory Pattern** (`factory.py`)
Implements the Factory pattern for creating models and views, providing:
- **Flexibility**: Easy swapping of different implementations
- **Extensibility**: Simple registration of custom components
- **Dependency Injection**: Loose coupling between components
- **Singleton Management**: Efficient instance reuse

## Benefits of MVC Refactoring

### ✅ **Separation of Concerns**
- **Model**: Pure business logic and data management
- **View**: Pure presentation and UI
- **Controller**: Pure application flow control

### ✅ **Maintainability**
- Each layer can be modified independently
- Clear boundaries between different responsibilities
- Easier to locate and fix bugs

### ✅ **Testability**
- Model classes can be unit tested without UI dependencies
- View components can be tested in isolation
- Controller logic can be tested independently

### ✅ **Reusability**
- Model classes can be reused in different contexts
- View components can be reused across different pages
- Controller patterns can be applied to other applications

### ✅ **Scalability**
- Easy to add new features by extending existing layers
- New AI models can be added to the Model layer
- New UI components can be added to the View layer

## File Structure

```
lovable/
├── __init__.py              # Python package marker
├── factory.py               # Factory pattern for component creation
├── models.py                # Model layer (data & business logic)
├── views.py                 # View layer (UI & presentation)
├── controller.py            # Controller layer (application flow)
├── streamlit_app.py         # Main application entry point
├── requirements.txt         # Dependencies
├── example_custom_components.py  # Example of using custom components
└── README_MVC.md           # This file
```

## How to Use

1. **Run the application**: `streamlit run streamlit_app.py`
2. **Modify business logic**: Edit `models.py`
3. **Change UI/styling**: Edit `views.py`
4. **Modify application flow**: Edit `controller.py`

## Adding New Features

### Adding a New AI Model
1. Create a new class in `models.py`
2. Implement the required interface
3. Update the controller to use the new model

### Adding a New Page
1. Create a new view class in `views.py`
2. Add navigation logic in `controller.py`
3. Update the main application flow

### Adding New Styling
1. Add CSS to the appropriate `CSSStyles` method in `views.py`
2. Apply the styles in the relevant view methods

## Migration Notes

The original monolithic `streamlit_app.py` has been completely refactored:
- All business logic moved to `models.py`
- All UI components moved to `views.py`
- All application flow moved to `controller.py`
- Main file now only contains the entry point

This refactoring maintains 100% of the original functionality while providing a much cleaner, more maintainable codebase.

## Factory Pattern Implementation

### 🏭 **Overview**
The Factory pattern has been implemented to provide flexible component creation and management. This allows for easy swapping of implementations and simple extension of the application.

### 🔧 **Key Components**

#### **BaseFactory** (Abstract)
- Abstract base class for all factories
- Defines the interface for component creation

#### **ModelFactory**
- Manages model class registrations
- Handles model instance creation
- Implements singleton pattern for efficient instance reuse

#### **ViewFactory**
- Manages view class registrations
- Handles view instance creation
- Implements singleton pattern for efficient instance reuse

#### **AppFactory**
- Main factory that coordinates model and view factories
- Automatically registers default components
- Provides methods for custom component registration

### 📝 **Usage Examples**

#### **Basic Usage**
```python
from factory import app_factory

# Create components using the factory
session = app_factory.create_model("ChatSession")
chat_view = app_factory.create_view("ChatView")
```

#### **Custom Component Registration**
```python
# Register custom models
app_factory.register_custom_model("CustomGenerator", CustomHTMLGenerator)

# Register custom views
app_factory.register_custom_view("CustomView", CustomChatView)
```

#### **Component Discovery**
```python
# See what components are available
available_models = app_factory.get_available_models()
available_views = app_factory.get_available_views()
```

### 🎯 **Benefits**

- **Loose Coupling**: Controller doesn't directly import model/view classes
- **Easy Testing**: Mock components can be easily swapped in
- **Extensibility**: New implementations can be added without modifying existing code
- **Maintainability**: Centralized component management
- **Performance**: Singleton pattern for stateless components

### 📚 **Example Implementation**
See `example_custom_components.py` for a complete example of how to create and register custom components with the factory.
