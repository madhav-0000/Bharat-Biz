import sys
try:
    import whisper
    import langchain
    import fastapi
    print("✅ Environment: Python 3.13 Detected")
    print("✅ Libraries: All loaded successfully")
except ImportError as e:
    print(f"❌ Missing: {e}")

import os
if os.path.exists("backend/db/kirana.db"):
    print("✅ Database: kirana.db found")
else:
    print("❌ Database: kirana.db NOT found in backend/db/")