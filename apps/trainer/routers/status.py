from fastapi import APIRouter
from tbmods.config import Config
from tbmods.cache import Cache

router = APIRouter(
    prefix="/status",
    tags=["status"],
)

config = Config()

@router.get('/')
def get_status():
    
    status = {}
    # config
    status['config'] = {
        'symbol':config['symbol'],
    }
    
    return status