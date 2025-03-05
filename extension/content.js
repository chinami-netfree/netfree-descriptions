// פונקציה להוספת כפתור התיאור
function addDescriptionButton() {
    // מציאת סרגל הכפתורים
    const toolbar = document.querySelector('app-add-to-ticket .btn-group');
    if (!toolbar) return;

    // יצירת הכפתור
    const button = document.createElement('button');
    button.className = 'btn btn-primary description-button';
    button.innerHTML = `
        <i class="fa fa-magic"></i>
        <span>הפק תיאור</span>
    `;

    // הוספת הכפתור לסרגל
    toolbar.appendChild(button);

    // הוספת מאזין לחיצה
    button.addEventListener('click', handleDescriptionButtonClick);
}

// פונקציה לטיפול בלחיצה על הכפתור
async function handleDescriptionButtonClick(event) {
    const button = event.currentTarget;
    const urlInput = document.querySelector('input[name="url"]');
    const contentTextarea = document.querySelector('textarea[name="content"]');

    // בדיקה שיש URL
    if (!urlInput?.value) {
        alert('נא להזין כתובת אתר');
        return;
    }

    try {
        // הצגת מצב טעינה
        button.classList.add('loading');

        // שליחת בקשה ל-Service Worker
        const response = await chrome.runtime.sendMessage({
            action: 'generateDescription',
            url: urlInput.value
        });

        if (response.success) {
            // הוספת התיאור לשדה ההודעה
            contentTextarea.value = response.description;
        } else {
            throw new Error(response.error);
        }
    } catch (error) {
        alert('שגיאה בהפקת התיאור: ' + error.message);
    } finally {
        // הסרת מצב טעינה
        button.classList.remove('loading');
    }
}

// הוספת הכפתור כשהדף נטען
function init() {
    // המתנה לטעינת הדף
    const observer = new MutationObserver((mutations, obs) => {
        const toolbar = document.querySelector('app-add-to-ticket .btn-group');
        if (toolbar) {
            addDescriptionButton();
            obs.disconnect();
        }
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// התחלת האתחול
init();