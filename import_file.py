import sys
import inspect
import pkgutil
if sys.version_info.major > 2:
    from importlib import reload
from imp import reload
import search
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from functools import partial
from search.agent import *
import search_list
import maps
from os import path