from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Dict
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from summary import scrape_website, summarize_content

# הגדרת הלימיטר
limiter = Limiter(key_func=get_remote_address)

# יצירת אפליקציית FastAPI
app = FastAPI(
    title="Web Description API",
    description="API להפקת תיאורים בעברית לאתרי אינטרנט",
    version="1.0.0"
)

# הוספת הלימיטר לאפליקציה
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# הגדרת CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # בסביבת ייצור יש להגדיר את הדומיינים המורשים
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# סכמות Pydantic
class SummarizeRequest(BaseModel):
    url: HttpUrl

class SummarizeResponse(BaseModel):
    url: HttpUrl
    description: str
    timestamp: datetime

class ErrorResponse(BaseModel):
    error: str
    error_code: str
    timestamp: datetime

# קודי שגיאה
class ErrorCodes:
    INVALID_URL = "INVALID_URL"
    SCRAPING_ERROR = "SCRAPING_ERROR"
    SUMMARY_ERROR = "SUMMARY_ERROR"
    RATE_LIMIT = "RATE_LIMIT"
    INTERNAL_ERROR = "INTERNAL_ERROR"

@app.get("/health")
def health_check() -> Dict[str, str]:
    """בדיקת בריאות בסיסית"""
    return {"status": "ok"}

@app.post("/api/v1/summarize", response_model=SummarizeResponse)
@limiter.limit("5/minute")
async def get_website_description(request: Request, summarize_request: SummarizeRequest) -> SummarizeResponse:
    """
    מקבל URL ומחזיר תיאור בעברית של תוכן האתר.
    מוגבל ל-5 בקשות בדקה לכל IP.
    """
    try:
        # גרידת האתר
        website_content = scrape_website(summarize_request.url)
        if not website_content:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "נכשלה גרידת האתר",
                    "error_code": ErrorCodes.SCRAPING_ERROR,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )

        # הפקת תקציר
        description = summarize_content(website_content)
        if not description:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "נכשלה הפקת התקציר",
                    "error_code": ErrorCodes.SUMMARY_ERROR,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )

        return SummarizeResponse(
            url=summarize_request.url,
            description=description,
            timestamp=datetime.now(timezone.utc)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "error_code": ErrorCodes.INTERNAL_ERROR,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
