import logging

from app.main import main

try:
    main()
except (KeyboardInterrupt, SystemExit):
    logging.info("Goodbye")
