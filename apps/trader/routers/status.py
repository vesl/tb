from fastapi import APIRouter
from tbmods.config import Config

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