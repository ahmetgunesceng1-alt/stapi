# Test Execution Results

Generated: 2026-04-08T12:15:38.280Z

================================================================================

Command: python tests/test_stapi_endpoints.py
Exit Code: 0

Output:
============================================================
API Test Suite
============================================================

Checking server connectivity...
✓ Server responding (status 200)


[TEST] GET / - Happy path
    ── Request ──
    GET https://stapi.co/
    ── Response ──
    Status: 200
    Body: <!DOCTYPE html><html lang="en"><head>
	<meta charset="utf-8">
	<title>STAPI, a Star Trek API</title>
	<base href="/">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="shortcut icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4QYEDwQag7x7MwAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAAq0lEQVQ4y82TMQrCQBBFXzYrWNiktvAU3mqPIx7FXhDsrAQFS0UrxaQRo5Ox...
  ✓ PASSED (status 200)

[TEST] Probe API index paths (/api, /v1)
    ── Request ──
    GET https://stapi.co/api
    ── Response ──
    Status: 200
    Body: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"><HTML><HEAD><LINK type="text/css" rel="stylesheet" href="/api/?stylesheet=1"><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>CXF - Service list</title></head><body><span class="heading">Available RESTful services:</span><br/><table cellpadding="1" cellspacing="1" border="1" width="100%"><tr><td><span class="field">Endpoint address:</span> <span class="value">http://stap...
  ✓ PASSED: /api (status 200)

[TEST] Discover collection and test single-resource retrieval

[DISCOVERY] Trying /api/people
    ── Request ──
    GET https://stapi.co/api/people
    ── Response ──
    Status: 404
    Body: <html><body>No service was found.</body></html>

[DISCOVERY] Trying /people
    ── Request ──
    GET https://stapi.co/people
    ── Response ──
    Status: 404
    Body: {"timestamp": 1775650533186, "status": 404, "error": "Not Found", "path": "/people"}

[DISCOVERY] Trying /api/characters
    ── Request ──
    GET https://stapi.co/api/characters
    ── Response ──
    Status: 404
    Body: <html><body>No service was found.</body></html>

[DISCOVERY] Trying /characters
    ── Request ──
    GET https://stapi.co/characters
    ── Response ──
    Status: 404
    Body: {"timestamp": 1775650533702, "status": 404, "error": "Not Found", "path": "/characters"}

[DISCOVERY] Trying /api/films
    ── Request ──
    GET https://stapi.co/api/films
    ── Response ──
    Status: 404
    Body: <html><body>No service was found.</body></html>

[DISCOVERY] Trying /films
    ── Request ──
    GET https://stapi.co/films
    ── Response ──
    Status: 404
    Body: {"timestamp": 1775650534238, "status": 404, "error": "Not Found", "path": "/films"}

[DISCOVERY] Trying /api/movies
    ── Request ──
    GET https://stapi.co/api/movies
    ── Response ──
    Status: 404
    Body: <html><body>No service was found.</body></html>

[DISCOVERY] Trying /movies
    ── Request ──
    GET https://stapi.co/movies
    ── Response ──
    Status: 404
    Body: {"timestamp": 1775650534728, "status": 404, "error": "Not Found", "path": "/movies"}
  ⚠ SKIPPED: No collection endpoint discovered

[TEST] POST to discovered collection (tolerant) 

[DISCOVERY] Trying /api/people
    ── Request ──
    GET https://stapi.co/api/people
    ── Response ──
    Status: 404
    Body: <html><body>No service was found.</body></html>

[DISCOVERY] Trying /people
    ── Request ──
    GET https://stapi.co/people
    ── Response ──
    Status: 404
    Body: {"timestamp": 1775650535271, "status": 404, "error": "Not Found", "path": "/people"}

[DISCOVERY] Trying /api/characters
    ── Request ──
    GET https://stapi.co/api/characters
    ── Response ──
    Status: 404
    Body: <html><body>No service was found.</body></html>

[DISCOVERY] Trying /characters
    ── Request ──
    GET https://stapi.co/characters
    ── Response ──
    Status: 404
    Body: {"timestamp": 1775650535808, "status": 404, "error": "Not Found", "path": "/characters"}

[DISCOVERY] Trying /api/films
    ── Request ──
    GET https://stapi.co/api/films
    ── Response ──
    Status: 404
    Body: <html><body>No service was found.</body></html>

[DISCOVERY] Trying /films
    ── Request ──
    GET https://stapi.co/films
    ── Response ──
    Status: 404
    Body: {"timestamp": 1775650536319, "status": 404, "error": "Not Found", "path": "/films"}

[DISCOVERY] Trying /api/movies
    ── Request ──
    GET https://stapi.co/api/movies
    ── Response ──
    Status: 404
    Body: <html><body>No service was found.</body></html>

[DISCOVERY] Trying /movies
    ── Request ──
    GET https://stapi.co/movies
    ── Response ──
    Status: 404
    Body: {"timestamp": 1775650536847, "status": 404, "error": "Not Found", "path": "/movies"}
  ⚠ SKIPPED: No collection endpoint discovered for POST

[TEST] Invalid auth header against root or discovered collection

[DISCOVERY] Trying /api/people
    ── Request ──
    GET https://stapi.co/api/people
    ── Response ──
    Status: 404
    Body: <html><body>No service was found.</body></html>

[DISCOVERY] Trying /people
    ── Request ──
    GET https://stapi.co/people
    ── Response ──
    Status: 404
    Body: {"timestamp": 1775650537340, "status": 404, "error": "Not Found", "path": "/people"}

[DISCOVERY] Trying /api/characters
    ── Request ──
    GET https://stapi.co/api/characters
    ── Response ──
    Status: 404
    Body: <html><body>No service was found.</body></html>

[DISCOVERY] Trying /characters
    ── Request ──
    GET https://stapi.co/characters
    ── Response ──
    Status: 404
    Body: {"timestamp": 1775650537840, "status": 404, "error": "Not Found", "path": "/characters"}

[DISCOVERY] Trying /api/films
    ── Request ──
    GET https://stapi.co/api/films
    ── Response ──
    Status: 404
    Body: <html><body>No service was found.</body></html>

[DISCOVERY] Trying /films
    ── Request ──
    GET https://stapi.co/films
    ── Response ──
    Status: 404
    Body: {"timestamp": 1775650538355, "status": 404, "error": "Not Found", "path": "/films"}

[DISCOVERY] Trying /api/movies
    ── Request ──
    GET https://stapi.co/api/movies
    ── Response ──
    Status: 404
    Body: <html><body>No service was found.</body></html>

[DISCOVERY] Trying /movies
    ── Request ──
    GET https://stapi.co/movies
    ── Response ──
    Status: 404
    Body: {"timestamp": 1775650538870, "status": 404, "error": "Not Found", "path": "/movies"}
    ── Request ──
    GET https://stapi.co/
    Headers: {"Authorization": "[REDACTED]"}
    ── Response ──
    Status: 200
    Body: <!DOCTYPE html><html lang="en"><head>
	<meta charset="utf-8">
	<title>STAPI, a Star Trek API</title>
	<base href="/">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="shortcut icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4QYEDwQag7x7MwAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAAq0lEQVQ4y82TMQrCQBBFXzYrWNiktvAU3mqPIx7FXhDsrAQFS0UrxaQRo5Ox...
  ✓ PASSED: Received status 200 with invalid token

============================================================
Results: 3 passed, 0 failed, 2 skipped
============================================================

================================================================================

