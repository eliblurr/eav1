from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/error")
async def show_logs():
    try:
        with open("get_exceptions_logger.log", "r") as logger:
            logs = ""
            logger.seek(0)
            for log in logger.readlines():
                logs = logs + log
            return logs
    except:
        raise HTTPException(status_code=307, detail="Temporary Redirect .... could not open file")