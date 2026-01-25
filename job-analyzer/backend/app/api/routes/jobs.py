from fastapi import APIRouter, HTTPException, status

from app.schemas.jobs import JobCreate, JobOut

router = APIRouter(prefix="/jobs", tags=["jobs"])

# Temporary in-memory store (good enough for Day 2 API structure).
_JOBS: dict[int, JobOut] = {}
_NEXT_ID = 1


@router.get("", response_model=list[JobOut])
def list_jobs() -> list[JobOut]:
    return list(_JOBS.values())


@router.post("", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate) -> JobOut:
    global _NEXT_ID
    job = JobOut(
        id=_NEXT_ID,
        title=payload.title,
        company=payload.company,
        description=payload.description,
        url=payload.url,
    )
    _JOBS[_NEXT_ID] = job
    _NEXT_ID += 1
    return job


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int) -> JobOut:
    job = _JOBS.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

