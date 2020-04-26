
from dotenv import load_dotenv

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
CONFIG_PATH = "../config/.env"
def load_env():
    load_dotenv(dotenv_path=CONFIG_PATH)

load_env()

# -------------------------------------------------
# Run Flask App
# -------------------------------------------------
from webApp import webApp

if __name__ == '__main__':
    webApp.run(port=8080, debug = True, use_reloader=False)
