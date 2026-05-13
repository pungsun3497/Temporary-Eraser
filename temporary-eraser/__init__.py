from krita import *
from .temporaryeraser import TemporaryEraser

Krita.instance().addExtension(TemporaryEraser(Krita.instance()))