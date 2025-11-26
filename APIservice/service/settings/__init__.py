import os
from dotenv import load_dotenv
load_dotenv()
if os.getenv("LEVEL") == "PROD":
    from .prod import *
else:
    from .settings import *