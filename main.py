#!/usr/bin/env python3
"""
XRD ANALYZER PRO plus v2.0
Complete XRD Analysis Suite - 20+ Formats, Touch Gestures, CSV Export, Multi-sheet Excel Export
"""

# ← CRITICAL: Set recursion limit BEFORE any other imports
import sys
import os
sys.setrecursionlimit(5000)

# ← CRITICAL: Helper function for PyInstaller bundled resource access (MODULE LEVEL)
def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    Use this for loading config.json, assets/, data/, etc.
    """
    if hasattr(sys, '_MEIPASS'):
        # Running as bundled executable
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ← Standard imports
import traceback
import logging
import json
from datetime import datetime

# ← Force matplotlib backend BEFORE importing pyplot
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# ← GUI imports
import tkinter as tk
from tkinter import messagebox, ttk

# Set up logging
log_file = f'xrd_debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_format)
logging.getLogger().addHandler(console_handler)

# Log system info
logging.info("=" * 50)
logging.info("XRD Analyzer Pro Startup")
logging.info(f"Python version: {sys.version}")
logging.info(f"Executable: {sys.executable}")
logging.info(f"Current directory: {os.getcwd()}")
logging.info(f"Script path: {__file__}")
logging.info(f"sys.path: {sys.path}")
logging.info("=" * 50)

try:
    # Add project root to path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    logging.info(f"Project root added to path: {project_root}")
    
    # Also add screens directory if it exists
    screens_path = os.path.join(project_root, 'screens')
    if os.path.exists(screens_path):
        if screens_path not in sys.path:
            sys.path.insert(0, screens_path)
        logging.info(f"Screens directory added to path: {screens_path}")
    else:
        # If screens folder doesn't exist, add current directory
        logging.info(f"Screens directory not found, using current directory")
    
    # Import custom modules - FIXED IMPORTS
    logging.info("Importing custom modules...")
    
    try:
        # Try importing from screens first
        try:
            from screens.home_screen import HomeScreen
            logging.info("✓ HomeScreen imported from screens/")
        except ImportError:
            # Fallback to current directory
            from home_screen import HomeScreen
            logging.info("✓ HomeScreen imported from current directory")
    except ImportError as e:
        logging.error(f"Failed to import HomeScreen: {str(e)}")
        logging.error(traceback.format_exc())
        raise
    
    try:
        try:
            from screens.graph_screen import GraphScreen
            logging.info("✓ GraphScreen imported from screens/")
        except ImportError:
            from graph_screen import GraphScreen
            logging.info("✓ GraphScreen imported from current directory")
    except ImportError as e:
        logging.error(f"Failed to import GraphScreen: {str(e)}")
        logging.error(traceback.format_exc())
        raise
    
    try:
        try:
            from screens.settings_screen import SettingsScreen
            logging.info("✓ SettingsScreen imported from screens/")
        except ImportError:
            from settings_screen import SettingsScreen
            logging.info("✓ SettingsScreen imported from current directory")
    except ImportError as e:
        logging.error(f"Failed to import SettingsScreen: {str(e)}")
        logging.error(traceback.format_exc())
    
    try:
        from data.data_manager import DataManager
        logging.info("✓ DataManager imported")
    except ImportError as e:
        logging.error(f"Failed to import DataManager: {str(e)}")
        logging.error(traceback.format_exc())
        raise
    
    logging.info("All imports successful!")
    
except Exception as e:
    error_msg = f"CRITICAL IMPORT ERROR: {str(e)}\n{traceback.format_exc()}"
    logging.critical(error_msg)
    
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Import Error", 
            f"Failed to import required modules:\n{str(e)}\n\n"
            f"Check {log_file} for details."
        )
        root.destroy()
    except:
        print(error_msg)
        print(f"Check {log_file} for details")
    
    sys.exit(1)


class XRDApplication:
    def __init__(self):
        logging.info("Initializing XRDApplication...")
        try:
            self.root = tk.Tk()
            logging.info("Tk root created")
            
            # Set application icon
            try:
                icon_path = get_resource_path("assets/icons/favicon.ico")
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
                    logging.info(f"Application icon set from: {icon_path}")
            except Exception as e:
                logging.warning(f"Could not set application icon: {e}")
            
            self.load_config()
            logging.info("Config loaded")
            
            self.root.title(f"{self.config['app_name']} v{self.config['version']}")
            self.root.geometry(self.config['gui']['home_size'])
            self.root.configure(bg="#f0f0f0")
            logging.info(f"Window configured: {self.config['app_name']} v{self.config['version']}")
            
            self.root.resizable(True, True)
            
            self.data_manager = DataManager()
            logging.info("DataManager initialized")
            
            self.current_screen = None
            self.setup_styles()
            logging.info("Styles setup complete")
            
            self.apply_theme()
            
            self.show_home_screen()
            logging.info("Home screen shown")
            
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            logging.info("XRDApplication initialization complete")
            
        except Exception as e:
            logging.error(f"Error in __init__: {str(e)}")
            logging.error(traceback.format_exc())
            raise

    def load_config(self):
        """Load configuration from config.json - PyInstaller compatible"""
        try:
            config_path = get_resource_path("config.json")
            logging.info(f"Loading config from: {config_path}")
            
            if not os.path.exists(config_path):
                logging.warning(f"config.json not found at {config_path}, using defaults")
                self.config = self._get_default_config()
                try:
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(self.config, f, indent=4)
                    logging.info(f"Default config saved to {config_path}")
                except:
                    pass
                return
                
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
            
            self._validate_config()
            logging.info(f"Config loaded successfully: {self.config.get('app_name')} v{self.config.get('version')}")
            
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in config.json: {str(e)}")
            messagebox.showerror("Configuration Error", 
                               f"Invalid configuration file format.\nUsing default settings.\n\nError: {str(e)}")
            self.config = self._get_default_config()
        except Exception as e:
            logging.error(f"Unexpected error loading config: {str(e)}")
            logging.error(traceback.format_exc())
            messagebox.showerror("Configuration Error", 
                               f"Failed to load configuration.\nUsing default settings.\n\nError: {str(e)}")
            self.config = self._get_default_config()

    def _validate_config(self):
        """Ensure config has all required sections"""
        default = self._get_default_config()
        
        for key in default:
            if key not in self.config:
                self.config[key] = default[key]
                logging.info(f"Added missing config key: {key}")
        
        if 'display' not in self.config:
            self.config['display'] = default['display']
            logging.info("Added missing display section to config")

    def _get_default_config(self):
        """Return default configuration dictionary"""
        return {
            "app_name": "XRD Analyzer Pro",
            "version": "2.0.0",
            "wavelength": 1.5406,
            "radiation": "Cu Kα",
            "default_2theta_range": [5.0, 150.0],
            "default_intensity_range": [0, 100],
            "peak_detection": {
                "min_intensity_percent": 5.0,
                "min_prominence": 2.0,
                "min_width": 3
            },
            "processing": {
                "smoothing_window": 7,
                "kalpha2_ratio": 0.5,
                "bg_granularity": 10,
                "bg_bending": 2
            },
            "gui": {
                "home_size": "1200x700",
                "graph_size": "1400x800",
                "theme": "light",
                "touch_enabled": True
            },
            "display": {
                "peak_display_limit": 0,
                "mineral_display_limit": 0,
                "intensity_threshold": 0,
                "show_grid": True,
                "show_references": True
            }
        }

    def setup_styles(self):
        """Setup color scheme and ttk styles"""
        try:
            self.colors = {
                "primary": "#2C3E50",
                "secondary": "#34495E",
                "accent": "#3498DB",
                "success": "#27AE60",
                "warning": "#F39C12",
                "danger": "#E74C3C",
                "light": "#ECF0F1",
                "dark": "#2C3E50",
                "background": "#F8F9FA",
            }
            
            style = ttk.Style()
            style.theme_use('clam')
            
            style.configure('TNotebook', background=self.colors['background'])
            style.configure('TNotebook.Tab', padding=[10, 5], font=('Arial', 10))
            style.map('TNotebook.Tab', 
                     background=[('selected', self.colors['accent'])],
                     foreground=[('selected', 'white')])
            
            style.configure('TButton', font=('Arial', 10), padding=5)
            style.configure('Success.TButton', background=self.colors['success'])
            style.configure('Danger.TButton', background=self.colors['danger'])
            
            logging.info("Styles setup complete")
        except Exception as e:
            logging.error(f"Error in setup_styles: {str(e)}")

    def apply_theme(self):
        """Apply theme based on config"""
        try:
            theme = self.config.get('gui', {}).get('theme', 'light')
            if theme == 'dark':
                self.root.configure(bg="#2C3E50")
            elif theme == 'blue':
                self.root.configure(bg="#3498DB")
            else:
                self.root.configure(bg="#f0f0f0")
            logging.info(f"Theme applied: {theme}")
        except Exception as e:
            logging.error(f"Error applying theme: {e}")

    def switch_screen(self, screen_class, **kwargs):
        """Switch between screens"""
        try:
            screen_name = screen_class.__name__
            logging.info(f"Switching to screen: {screen_name}")
            
            for widget in self.root.winfo_children():
                widget.destroy()
            
            self.current_screen = screen_class(self.root, self, **kwargs)
            self.current_screen.pack(fill=tk.BOTH, expand=True)
            
            if screen_name == "HomeScreen":
                self.root.title(f"{self.config['app_name']} - Home")
            elif screen_name == "GraphScreen":
                self.root.title(f"{self.config['app_name']} - XRD Analysis")
            elif screen_name == "SettingsScreen":
                self.root.title(f"{self.config['app_name']} - Settings")
            
            logging.info(f"Screen switch to {screen_name} successful")
            
        except Exception as e:
            logging.error(f"Error switching to screen {screen_class.__name__}: {str(e)}")
            logging.error(traceback.format_exc())
            messagebox.showerror("Screen Error", f"Failed to load screen: {str(e)}")
            try:
                self.show_home_screen()
            except:
                pass

    def show_home_screen(self):
        """Show home screen"""
        try:
            logging.info("Showing home screen")
            self.root.geometry(self.config["gui"]["home_size"])
            self.switch_screen(HomeScreen)
            logging.info("Home screen displayed")
        except Exception as e:
            logging.error(f"Error showing home screen: {str(e)}")
            logging.error(traceback.format_exc())
            messagebox.showerror("Error", f"Failed to show home screen: {str(e)}")

    def show_graph_screen(self):
        """Show graph screen with data"""
        try:
            logging.info("Showing graph screen")
            if self.data_manager.current_data:
                self.root.geometry(self.config["gui"]["graph_size"])
                self.switch_screen(GraphScreen, data=self.data_manager.current_data)
                logging.info("Graph screen displayed with data")
            else:
                logging.warning("Attempted to show graph screen with no data")
                messagebox.showwarning("No Data", "Please load XRD data first")
                self.show_home_screen()
        except Exception as e:
            logging.error(f"Error showing graph screen: {str(e)}")
            logging.error(traceback.format_exc())
            messagebox.showerror("Error", f"Failed to show graph screen: {str(e)}")

    def show_settings_screen(self):
        """Show settings screen"""
        try:
            logging.info("Showing settings screen")
            self.switch_screen(SettingsScreen)
            logging.info("Settings screen displayed")
        except Exception as e:
            logging.error(f"Error showing settings screen: {str(e)}")
            logging.error(traceback.format_exc())
            messagebox.showerror("Error", f"Failed to show settings screen: {str(e)}")

    def on_closing(self):
        """Handle window closing"""
        try:
            logging.info("Application closing...")
            if messagebox.askokcancel("Quit", "Exit XRD Analyzer Pro?"):
                logging.info("User confirmed exit")
                
                if hasattr(self, 'data_manager'):
                    self.data_manager.save_session()
                    logging.info("Session saved")
                
                try:
                    config_path = get_resource_path("config.json")
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(self.config, f, indent=4)
                    logging.info("Config saved on exit")
                except Exception as e:
                    logging.warning(f"Could not save config on exit: {e}")
                
                logging.info("Application closed successfully")
                self.root.destroy()
            else:
                logging.info("Exit cancelled by user")
        except Exception as e:
            logging.error(f"Error during closing: {str(e)}")
            logging.error(traceback.format_exc())
            self.root.destroy()

    def run(self):
        """Run the application"""
        try:
            logging.info("Starting main loop")
            self.root.mainloop()
            logging.info("Main loop ended")
        except Exception as e:
            logging.error(f"Error in main loop: {str(e)}")
            logging.error(traceback.format_exc())
            messagebox.showerror("Runtime Error", f"Application error: {str(e)}")


if __name__ == "__main__":
    try:
        logging.info("Creating application instance...")
        app = XRDApplication()
        logging.info("Running application...")
        app.run()
    except Exception as e:
        error_msg = f"FATAL ERROR: {str(e)}\n{traceback.format_exc()}"
        logging.critical(error_msg)
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Fatal Error", 
                f"The application failed to start:\n{str(e)}\n\n"
                f"Check {log_file} for details."
            )
            root.destroy()
        except:
            print(error_msg)
            print(f"Check {log_file} for details")
        
        sys.exit(1)