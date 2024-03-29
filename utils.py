from datetime import datetime, timedelta
# from compress import Compressor
from typing import Optional
import shutil, logging, jwt, os, string, random
from constants import switcher

SECRET_KEY = "fsdfsdfsdfsdflhiugysadf87w940e-=r0werpolwe$16$5*dfsdfsdf&&#$rrr$$)7a9563OO93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

uppercase_and_digits = string.ascii_uppercase + string.digits
lowercase_and_digits = string.ascii_lowercase + string.digits

# compression = Compressor()
# compression.use_gzip() # or use_bz2, use_lzma, use_lz4, use_snappy

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=40)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(*, data: str):
    to_decode = data
    return jwt.decode(to_decode, SECRET_KEY, algorithm=ALGORITHM)

def time_difference(start_date):
    delta = datetime.now()-start_date
    return delta.total_seconds()

def gen_alphanumeric_code(length):
    code = ''.join((random.choice(uppercase_and_digits) for i in range(length)))
    return code

def gen_alphanumeric_code_lower(length):
    code = ''.join((random.choice(lowercase_and_digits) for i in range(length)))
    return code

async def folder_exists(directory):
    return os.path.isdir(directory)

async def file_exists(path):
    try:
        return os.path.isfile(path)
    except:
        return False

async def create_file(url,image):
    try:
        with open('{url}'.format(url=url), 'wb') as new_image:
            new_image.write(image)
        return True
    except:
        return False

async def delete_file(url):
    try:
        os.remove(url)
        return True
    except:
        return False

async def create_folder(url):
    try:
        os.mkdir(url)
        return True
    except:
        return False
    
async def delete_folder(url):
    try:
        shutil.rmtree(url)
        return True
    except:
        return False

async def compress_file(binary_data):
    try:
        await compression.compress(binary_data, zlib_level=9)
        return True
    except:
        return False

async def decompress_file(binary_data):
    try:
        await compression.decompress(binary_data)
        return True
    except:
        return False  

async def len_of_dir_children(dir_path):
    try:
        length = await len(os.listdir(dir_path))
        return length
    except:
        return False

def logical_xor(str1, str2):
    return bool(str1) ^ bool(str2)

async def string_list_to_int_list(str_list:list):
    int_list = []
    for item in str_list:
        if item.isdigit():
            int_list.append(int(item))
    return int_list

def get_exceptions_logger():
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler = logging.FileHandler('exceptions_logs.log', mode='a')
    handler.setLevel(level=logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def get_currency(code):
    return switcher.get(code)