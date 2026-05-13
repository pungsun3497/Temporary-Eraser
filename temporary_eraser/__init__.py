from krita import *
from .temporary_eraser import TemporaryEraser

Krita.instance().addExtension(TemporaryEraser(Krita.instance()))