import logging
import os

logger = logging.getLogger(__name__)

def setup_logger():
    worker_id = os.environ.get("PYTEST_XDIST_WORKER")
    filename = "logs/test.log"
    if worker_id is not None:
        filename = f"logs/test_{worker_id}.log"
    logging.basicConfig(filename=filename, 
                        level=logging.INFO, 
                        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")



