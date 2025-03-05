# Description API for Netfree

מערכת להפקת תיאורים אוטומטיים בעברית עבור אתרי אינטרנט, לשימוש בממשק בקשות הפתיחה של Netfree.

## תיאור המערכת

המערכת מורכבת משני חלקים עיקריים:
1. **API להפקת תיאורים** - שירות המקבל URL ומחזיר תיאור בעברית
2. **תוסף דפדפן** - מאפשר הפקת תיאור אוטומטי בטופס הבקשות של Netfree

### יכולות עיקריות
- גרידת תוכן אתרים באמצעות Firecrawl
- הפקת תיאורים בעברית באמצעות OpenAI
- הגבלת קצב בקשות (5 בקשות לדקה לכל IP)
- תמיכה בהפעלה בדוקר

## התקנה

### דרישות מקדימות
- Docker ו-Docker Compose
- מפתח API של OpenAI

### שלבי ההתקנה

1. שכפול המאגר:
```bash
git clone [URL]
cd [REPO_NAME]
```

2. הגדרת משתני סביבה:
```bash
# .env
OPENAI_API_KEY=your-openai-api-key
```

3. בניית והרצת המערכת:
```bash
docker-compose -f docker-compose.descriptions.yml up -d
```

## שימוש ב-API

### נקודות קצה

#### בדיקת בריאות
```bash
GET /health
```

תגובה:
```json
{
    "status": "ok"
}
```

#### הפקת תיאור
```bash
POST /api/v1/summarize
Content-Type: application/json

{
    "url": "https://example.com"
}
```

תגובה:
```json
{
    "url": "https://example.com",
    "description": "תיאור האתר בעברית",
    "timestamp": "2024-03-04T23:51:03.683419Z"
}
```

### דוגמה לשימוש

```bash
curl -X POST http://localhost:8000/api/v1/summarize \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## מבנה הפרויקט

```
.
├── app.py                    # שרת FastAPI
├── summary.py               # לוגיקת הפקת התיאורים
├── requirements.txt         # תלויות Python
├── descriptions.Dockerfile  # הגדרות Docker
├── docker-compose.descriptions.yml  # הגדרות Docker Compose
└── extension/              # תוסף הדפדפן
    ├── manifest.json
    ├── content.js
    ├── service-worker.js
    └── style.css
```

## תוסף הדפדפן

התוסף מוסיף כפתור "הפק תיאור" לטופס הבקשות של Netfree. לחיצה על הכפתור:
1. גורדת את האתר המבוקש
2. מפיקה תיאור בעברית
3. מוסיפה את התיאור לשדה ההודעה בטופס

### התקנת התוסף
1. פתח את כרום והכנס לכתובת `chrome://extensions`
2. הפעל "מצב מפתח"
3. לחץ על "טען תוסף שלא ארוז" ובחר את תיקיית `extension`

## הגדרות

כל ההגדרות נקבעות באמצעות משתני סביבה:

| משתנה | תיאור | ברירת מחדל |
|--------|-----------|---------|
| `OPENAI_API_KEY` | מפתח API של OpenAI | חובה |
| `FIRECRAWL_API_URL` | כתובת שירות Firecrawl | `http://api:3002` |

## פתרון בעיות

1. **שגיאת חיבור ל-API**:
   - ודא שכל השירותים רצים: `docker-compose -f docker-compose.descriptions.yml ps`
   - בדוק לוגים: `docker-compose -f docker-compose.descriptions.yml logs -f description-api`

2. **שגיאות גרידה**:
   - ודא שהאתר נגיש
   - בדוק את לוגים של Firecrawl

3. **שגיאות OpenAI**:
   - ודא שמפתח ה-API תקין
   - בדוק מכסת שימוש

## מידע נוסף

- המערכת מגבילה ל-5 בקשות בדקה לכל IP
- התיאורים נוצרים באמצעות מודל GPT של OpenAI
- הגרידה מתבצעת באמצעות Firecrawl
- התוסף תומך בכרום ובדפדפנים מבוססי כרומיום