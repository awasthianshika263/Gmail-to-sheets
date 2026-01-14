# Gmail to Google Sheets Automation

## Author
Anshika Awasthi

---

## 📌 Project Overview
This project is a Python-based automation system that reads **real unread emails** from a Gmail inbox using the **Gmail API** and logs relevant email details into a **Google Sheet** using the **Google Sheets API**.

The system is designed to be **idempotent** — running it multiple times will not create duplicate entries. Once processed, emails are marked as **read** to prevent reprocessing.

---

## 🎯 Objective
For every qualifying email, the script appends a new row in Google Sheets with the following fields:

| Column | Description |
|------|------------|
| From | Sender email address |
| Subject | Email subject |
| Date | Date & time received |
| Content | Email body (plain text) |

---

## 🧠 High-Level Architecture

```
Gmail Inbox (Unread Emails)
        ↓
Gmail API (OAuth 2.0)
        ↓
Python Automation Script
        ↓
Google Sheets API
        ↓
Google Sheet (Append Rows)
```

---

## ⚙️ Tech Stack
- Python 3
- Gmail API
- Google Sheets API
- OAuth 2.0 (Desktop Application)

---

## 📂 Project Structure

```
gmail-to-sheets/
│
├── src/
│   ├── gmail_service.py      # Gmail authentication & email fetching
│   ├── sheets_service.py    # Google Sheets authentication & data append
│   ├── email_parser.py      # Email content parsing logic
│   └── main.py              # Application entry point
│
├── credentials/
│   └── credentials.json     # OAuth credentials (NOT committed)
│
├── config.py                # API scopes, Sheet ID, config values
├── requirements.txt
├── README.md
```

---

## 🔐 OAuth 2.0 Authentication Flow

1. User runs the script for the first time
2. Browser opens Google OAuth consent screen
3. User grants Gmail and Sheets permissions
4. Google returns an authorization code
5. Access & refresh tokens are stored locally (`token.json`)
6. Tokens are reused for future runs until expired

**Why OAuth instead of Service Account?**  
Gmail API does not support service accounts for personal inbox access. OAuth 2.0 is mandatory.

---

## 📥 Email Fetching Logic

- Only emails from:
  - Inbox
  - Unread (`is:unread`)

Gmail API query used:
```
is:unread in:inbox
```

After successful processing, each email is marked as **read** using the Gmail API.

---

## ✂️ Email Parsing Logic

The Gmail API returns email data in a nested MIME format.

Parsing steps:
- Extract `From`, `Subject`, and `Date` from email headers
- Decode the email body from Base64
- Convert HTML content to plain text if required

Parsing is isolated in `email_parser.py` to maintain separation of concerns.

---

## 🚫 Duplicate Prevention Logic

Duplicate entries are prevented using **state persistence**.

### Approach Used:
- The script stores the **last processed email timestamp (`internalDate`)** in a local file (`state.json`)
- On subsequent runs, only emails received *after* this timestamp are processed

### Why this approach?
- Efficient for large inboxes
- Avoids storing hundreds of message IDs
- Ensures idempotent behavior across runs

---

## 💾 State Persistence

- State is stored locally in a JSON file
- Updated after every successful email append

This ensures:
- Script restarts are safe
- No email is processed twice

---

## ▶️ Execution Flow

1. Authenticate Gmail API
2. Fetch unread emails
3. Parse required fields
4. Append rows to Google Sheet
5. Mark emails as read
6. Update processing state

---

## 🧪 Proof of Execution

Included inside `/proof/` folder:

### Screenshots
- Gmail inbox showing unread emails
- Google Sheet populated with at least 5 rows
- OAuth consent screen

### Video (2–3 minutes)
- End-to-end flow explanation
- Duplicate prevention demo
- Re-run behavior demonstration

---

## ⚠️ Challenges Faced

**Challenge:** Parsing Gmail email body reliably due to MIME complexity

**Solution:**
Handled multipart payloads and selectively decoded `text/plain` parts. Added fallback logic for HTML-only emails.

---

## 🚧 Limitations

- Does not handle email attachments
- Requires manual OAuth consent on first run
- Gmail API quota limits apply

---

## 🔄 Post-Submission Modification Readiness

The project structure allows easy enhancements such as:
- Time-based filtering (last 24 hours)
- Label-based filtering
- Additional columns without schema changes

---

## 🚫 Security Compliance

- `credentials.json` is excluded via `.gitignore`
- OAuth tokens are never committed
- No secrets are hardcoded

---

## ✅ Conclusion

This project demonstrates real-world API integration, authentication handling, state management, and clean code structure suitable for production-grade automation.

