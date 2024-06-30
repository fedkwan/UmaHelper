import os
import logging
import onnxruntime as ort

ort.set_default_logger_severity(3)

logging.getLogger("airtest").setLevel(logging.ERROR)
logging.getLogger("ppocr").setLevel(logging.ERROR)
logging.getLogger("ddddocr").setLevel(logging.ERROR)


DEFAULT_SLEEP_TIME = 0.5
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

