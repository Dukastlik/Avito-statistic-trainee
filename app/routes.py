from fastapi import APIRouter, BackgroundTasks, status
from api.add import register_new_query
from models.requestmodel import AddRequest, StatRequest
from api.get_stat import get_stat
from api.update import update_query


router = APIRouter()


@router.post('/add', status_code=status.HTTP_201_CREATED)
async def add_stat(request: AddRequest, background_tasks: BackgroundTasks) -> dict:
    new_query_id = await register_new_query(request.query, request.region)

    # Background_tasks here is not the best idea, it provides quick solution with bigger limitations.
    # Should instead use celery or cron for scheduling further.
    background_tasks.add_task(
        update_query, str(new_query_id), request.query, request.region, background_tasks
    )
    return {"new_id": str(new_query_id)}


@router.get('/stat')
async def retrieve_stat(request: StatRequest) -> dict:
    response = await get_stat(request.id, request.start_time, request.end_time)
    return response
