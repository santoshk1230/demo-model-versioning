import hashlib
from datetime import datetime
import warnings 

warnings.filterwarnings('ignore')


def generate_unique_id(email,phone,pan):
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")  # Timestamp with microseconds
        unique_string = f"{email}{phone}{pan}{timestamp}"
        return hashlib.sha256(unique_string.encode()).hexdigest()
    except Exception as e:
        print('unable to generate unique id for customer. please check given details')
        print('exception occured: ',e)