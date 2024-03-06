from pydantic import BaseModel


class ImdbData(BaseModel):
    isAdult: int
    runtimeMinutes: int
    averageRating: float
    numVotes: int
    budget: int
    release_year: int
    release_month: int
    release_day: int
    Adventure: int
    Animation: int
    Drama: int
    Action: int
    Crime: int