# How to Work with the URL‑Shortener Project

## 1️⃣ Project layout
```
(gogle‑weektwe)
│   index.html          # front‑end page with URL input form
│   requirements.txt    # Python deps (flask, pytest)
│   prompt.txt          # original assignment description
│   how_to_work.md      # **this** file
│
├─ src
│   │   __init__.py
│   │   app.py          # Flask entry point (serves UI & API)
│   │   service.py      # Business logic (create/resolve URLs)
│   │   storage.py      # In‑memory store with TTL
│
└─ tests
    │   test_service.py # pytest suite – TDD core tests
```

## 2️⃣ Prerequisites
- **Windows 10/11** with **Python 3.11+** installed and added to `PATH`.
- Internet access to download the packages listed in `requirements.txt`.

## 3️⃣ One‑time setup (optional but recommended)
Open **Command Prompt** **or** **PowerShell**, navigate to the project root, then create a virtual environment:

```cmd
cd C:\Users\lee73\Desktop\goluglel\gogle‑weektwe
python -m venv .venv
\.venv\Scripts\activate.bat   # Cmd
# or
# .\.venv\Scripts\Activate.ps1   # PowerShell (may need Set‑ExecutionPolicy Bypass)
```

## 4️⃣ Install dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
You should see `flask` and `pytest` installed.

## 5️⃣ Verify the core logic (TDD)
Run the unit‑test suite:
```bash
python -m pytest
```
**Expected result:**
```
============================= test session starts ==============================
collected 4 items

tests/test_service.py ....                                            [100%]

============================== 4 passed in X.XXs ==============================
```
If any test fails, copy the traceback and check imports or the `src/` path.

## 6️⃣ Start the development server
```bash
python -m src.app
```
You will see:
```
 * Serving Flask app "src.app"
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
Leave this terminal open – the server must keep running.

## 7️⃣ Test the UI
Open a browser and go to:
```
http://127.0.0.1:5000/
```
You should see the marketing page with a **“Create a Short Link”** form. Enter a long URL and click **Shorten** – a clickable short URL will appear.

## 8️⃣ Test the API manually
You can use **curl** (built‑in on Windows 10+) or PowerShell’s `Invoke‑RestMethod`.

### 8.1 Create a short link
**Cmd (curl)**
```cmd
curl -X POST http://127.0.0.1:5000/shorten ^
     -H "Content-Type: application/json" ^
     -d "{\"url\":\"https://example.com\"}"
```
**PowerShell**
```powershell
$body = @{ url = 'https://example.com' } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:5000/shorten -Method Post -ContentType 'application/json' -Body $body
```
You will receive JSON with `short_key` and `short_url`.

### 8.2 Resolve (redirect)
Replace `<short_key>` with the key you got.
**Cmd (curl with follow‑redirect)**
```cmd
curl -L http://127.0.0.1:5000/<short_key>
```
**PowerShell**
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000/<short_key> -MaximumRedirection 5
```
The request should end up at the original URL.

### 8.3 Get statistics
**Cmd**
```cmd
curl http://127.0.0.1:5000/stats/<short_key>
```
**PowerShell**
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/stats/<short_key>
```
Typical response:
```json
{
  "original_url": "https://example.com",
  "access_count": 1,
  "expires_at": "2026-05-10T15:45:00"
}
```

## 9️⃣ Optional: Quick TTL test
1. Edit `src/service.py` and set `ttl=timedelta(seconds=5)` when creating `URLService`.
2. Restart the server, create a short link, wait > 5 s, then try to resolve – you should get a **404** (expired).

## 10️⃣ Clean‑up
- Stop the Flask server (`Ctrl+C`).
- Deactivate the virtual environment: `deactivate` (both shells).
- Delete the `.venv` folder if you no longer need it.

---
### TL;DR
1. `cd …\gogle‑weektwe`<br>2. *(optional)* `python -m venv .venv && .venv\Scripts\activate.bat`<br>3. `python -m pip install -r requirements.txt`<br>4. `python -m pytest` (all green) <br>5. `python -m src.app` (keep running) <br>6. Browse to `http://127.0.0.1:5000/` or use the curl/PowerShell commands above.

Now anyone can clone the folder, follow these steps, and have the same working URL‑shortener.
