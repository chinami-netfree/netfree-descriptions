// הגדרת כתובת ה-API
const API_URL = 'http://localhost:8000/api/v1/summarize';

// טיפול בבקשות מה-content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'generateDescription') {
        generateDescription(request.url)
            .then(description => sendResponse({ success: true, description }))
            .catch(error => sendResponse({ success: false, error: error.message }));
        return true; // מציין שהתשובה תישלח באופן אסינכרוני
    }
});

// פונקציה להפקת תיאור מה-API
async function generateDescription(url) {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url })
        });

        if (!response.ok) {
            throw new Error('שגיאה בהפקת התיאור');
        }

        const data = await response.json();
        return data.description;
    } catch (error) {
        console.error('Error generating description:', error);
        throw new Error('שגיאה בהפקת התיאור מהשרת');
    }
}