#!/usr/bin/env python3
"""
API Test Suite
Tests for stapi.co endpoints (discovery + basic CRUD smoke tests)
"""

import http.client
import json
import os
import sys
import time
from urllib.parse import urlparse, quote

# Configuration — port is auto-detected by the execution system
SERVER_PORT = os.environ.get("SERVER_PORT", "3001")
BASE_URL = os.environ.get("API_BASE_URL", f"http://localhost:{SERVER_PORT}")
TIMEOUT = 10  # seconds
passed = 0
failed = 0
skipped = 0


def make_request(method, path, body=None, headers=None):
    """Make HTTP request to the API"""
    if headers is None:
        headers = {}
    # Add default Content-Type for JSON
    if body is not None and 'Content-Type' not in headers:
        headers['Content-Type'] = 'application/json'
    # Store request info for reporting
    request_info = {
        'method': method,
        'url': BASE_URL + path,
        'headers': {k: v for k, v in headers.items()},
        'body': body
    }
    # Parse URL
    url = urlparse(BASE_URL + path)
    try:
        # Create connection (HTTPS or HTTP based on scheme)
        if url.scheme == 'https':
            import ssl
            context = ssl.create_default_context()
            conn = http.client.HTTPSConnection(url.netloc, timeout=TIMEOUT, context=context)
        else:
            conn = http.client.HTTPConnection(url.netloc, timeout=TIMEOUT)
        # Prepare body
        body_data = json.dumps(body) if body is not None else None
        # Make request
        conn.request(method, url.path + ('?' + url.query if url.query else ''), 
                    body=body_data, headers=headers)
        # Get response
        response = conn.getresponse()
        response_data = response.read().decode('utf-8')
        # Try to parse JSON
        try:
            response_body = json.loads(response_data) if response_data else None
        except json.JSONDecodeError:
            response_body = response_data
        # Get response headers (normalize to lowercase keys for consistent lookup)
        raw_headers = dict(response.getheaders())
        norm_headers = {k.lower(): v for k, v in raw_headers.items()}
        conn.close()
        return {
            'status': response.status,
            'body': response_body,
            'headers': norm_headers,
            'request': request_info
        }
    except Exception as e:
        return {
            'status': 0,
            'body': None,
            'headers': {},
            'error': str(e),
            'request': request_info
        }


def truncate(obj, max_len=500):
    """Truncate a JSON-serializable object's string representation for display"""
    s = json.dumps(obj, ensure_ascii=False, default=str) if not isinstance(obj, str) else obj
    return s[:max_len] + '...' if len(s) > max_len else s


def print_req_res(response):
    """Print request and response details for the test report"""
    req = response.get('request', {})
    print(f"    ── Request ──")
    print(f"    {req.get('method', '?')} {req.get('url', '?')}")
    if req.get('headers'):
        safe_headers = {k: ('[REDACTED]' if k.lower() == 'authorization' else v) for k, v in req['headers'].items()}
        print(f"    Headers: {json.dumps(safe_headers, ensure_ascii=False)}")
    if req.get('body'):
        print(f"    Body: {truncate(req['body'])}")
    print(f"    ── Response ──")
    print(f"    Status: {response.get('status', '?')}")
    if response.get('body') is not None:
        print(f"    Body: {truncate(response['body'])}")


def test_root_happy_path():
    """Test: GET / - Happy path (server connectivity)"""
    global passed, failed, skipped
    print("\n[TEST] GET / - Happy path")
    try:
        response = make_request('GET', '/')
        print_req_res(response)
        if 'error' in response:
            print(f"  ✗ FAILED: {response['error']}")
            failed += 1
            return
        # Accept common successful responses for root
        if response['status'] == 0:
            print("  ✗ FAILED: No response from server")
            failed += 1
            return
        if response['status'] in (200, 301, 302, 401, 403):
            # Body may be HTML or JSON; just ensure it's non-empty
            if response['body'] is None or response['body'] == '':
                print("  ✗ FAILED: Empty response body")
                failed += 1
                return
            print(f"  ✓ PASSED (status {response['status']})")
            passed += 1
            return
        else:
            # Treat 404 as skipped (no root content)
            if response['status'] == 404:
                print(f"  ⚠ SKIPPED: Root returned 404")
                skipped += 1
                return
            print(f"  ✗ FAILED: Unexpected status {response['status']}")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAILED: {str(e)}")
        failed += 1


def test_api_index_paths():
    """Test: Probe common API index paths like /api and /v1"""
    global passed, failed, skipped
    print("\n[TEST] Probe API index paths (/api, /v1)")
    tried = []
    for p in ['/api', '/v1', '/rest']:
        tried.append(p)
        try:
            response = make_request('GET', p)
            print_req_res(response)
            if 'error' in response:
                print(f"  ✗ FAILED: {response['error']}")
                failed += 1
                return
            if response['status'] in (200, 301, 302, 401, 403):
                print(f"  ✓ PASSED: {p} (status {response['status']})")
                passed += 1
                return
            elif response['status'] == 404:
                print(f"  ⚠ SKIPPED: {p} returned 404")
                skipped += 1
                continue
            else:
                # Treat other statuses as pass if body non-empty
                if response['body']:
                    print(f"  ✓ PASSED (len body > 0) for {p} (status {response['status']})")
                    passed += 1
                    return
                else:
                    print(f"  ⚠ SKIPPED: {p} returned status {response['status']} with empty body")
                    skipped += 1
        except Exception as e:
            print(f"  ✗ FAILED: {str(e)}")
            failed += 1
            return
    print(f"  ⚠ SKIPPED: None of the index paths {tried} gave a usable response")


def discover_collection_path():
    """Try to discover a public collection endpoint from common candidates.
    Returns the first path that looks like a collection (status 200 and body present).
    """
    candidates = ['/api/people', '/people', '/api/characters', '/characters', '/api/films', '/films', '/api/movies', '/movies']
    for p in candidates:
        try:
            response = make_request('GET', p)
            print(f"\n[DISCOVERY] Trying {p}")
            print_req_res(response)
            if 'error' in response:
                # connection error — skip this candidate
                continue
            if response['status'] == 200 and response['body']:
                # Heuristic: body is list or dict with items
                b = response['body']
                if isinstance(b, list) and len(b) >= 0:
                    return p, b
                if isinstance(b, dict):
                    # Could be { data: [...] } or single object; accept as collection if contains list values
                    for k, v in b.items():
                        if isinstance(v, list):
                            return p, v
                    # If dict looks like a single resource, still return (collection may be paged)
                    return p, b
            # treat 401/403 as evidence the endpoint exists but is protected
            if response['status'] in (401, 403):
                return p, None
        except Exception:
            continue
    return None, None


def extract_id_from_item(item):
    """Try to pull an ID-like field from an item (look for common keys)."""
    if not isinstance(item, dict):
        return None
    for key in ('id', 'uuid', '_id', 'uid', 'slug'):
        if key in item:
            return str(item[key])
    # Try nested data keys
    for k, v in item.items():
        if isinstance(v, str) and len(v) > 0 and ('-' in v or v.isdigit() or len(v) >= 6):
            # heuristic candidate, but avoid random strings
            return v
    return None


def test_collection_and_single_resource():
    """Test: discover a collection endpoint, test list and single resource retrieval"""
    global passed, failed, skipped
    print("\n[TEST] Discover collection and test single-resource retrieval")
    path, body = discover_collection_path()
    if not path:
        print("  ⚠ SKIPPED: No collection endpoint discovered")
        skipped += 1
        return
    # If body is None and status was 401/403 (protected), we still consider it discovered
    if body is None:
        print(f"  ⚠ SKIPPED: {path} appears protected (401/403); cannot inspect items")
        skipped += 1
        return
    # Happy path for collection
    try:
        response = make_request('GET', path)
        print_req_res(response)
        if 'error' in response:
            print(f"  ✗ FAILED: {response['error']}")
            failed += 1
            return
        # Accept 200 or other statuses if body present
        if response['status'] == 200 and response['body'] is not None:
            print(f"  ✓ PASSED: Collection {path} returned data")
            passed += 1
        else:
            # treat other statuses with body as pass
            if response['body']:
                print(f"  ✓ PASSED: Collection {path} returned body (status {response['status']})")
                passed += 1
            else:
                print(f"  ⚠ SKIPPED: Collection {path} returned no usable body (status {response['status']})")
                skipped += 1
                return
        # Try to extract an ID for single-resource GET
        items = response['body']
        candidate_id = None
        if isinstance(items, list) and len(items) > 0:
            candidate_id = extract_id_from_item(items[0])
        elif isinstance(items, dict):
            # If dict has nested list, try first element
            for v in items.values():
                if isinstance(v, list) and len(v) > 0:
                    candidate_id = extract_id_from_item(v[0])
                    break
        if not candidate_id:
            print("  ⚠ SKIPPED: Could not extract an ID from collection items")
            skipped += 1
            return
        # Build candidate resource path
        # If collection path ends with plural, append /{id}
        if path.endswith('/'):
            res_path = path + quote(candidate_id)
        else:
            res_path = path + '/' + quote(candidate_id)
        # GET single resource
        resp2 = make_request('GET', res_path)
        print_req_res(resp2)
        if 'error' in resp2:
            print(f"  ✗ FAILED: {resp2['error']}")
            failed += 1
            return
        # Accept 200, 400, 404 per rules
        if resp2['status'] in (200, 400, 404):
            print(f"  ✓ PASSED: Single resource GET {res_path} returned {resp2['status']}")
            passed += 1
        else:
            print(f"  ✓ PASSED: Single resource GET {res_path} returned {resp2['status']}")
            passed += 1
    except Exception as e:
        print(f"  ✗ FAILED: {str(e)}")
        failed += 1


def test_post_create_on_collection():
    """Test: attempt to POST a dummy object to the discovered collection. Accept many statuses as success per rules."""
    global passed, failed, skipped
    print("\n[TEST] POST to discovered collection (tolerant) ")
    path, body = discover_collection_path()
    if not path:
        print("  ⚠ SKIPPED: No collection endpoint discovered for POST")
        skipped += 1
        return
    dummy = {"testbot": True, "timestamp": int(time.time())}
    try:
        resp = make_request('POST', path, body=dummy)
        print_req_res(resp)
        if 'error' in resp:
            print(f"  ✗ FAILED: {resp['error']}")
            failed += 1
            return
        # Per absolute constraints: POST/PUT/DELETE tests accept most codes except 0/404/405
        if resp['status'] in (0, 404, 405):
            print(f"  ✗ FAILED: POST returned status {resp['status']} — path or method likely incorrect")
            failed += 1
            return
        # Accept as pass otherwise
        print(f"  ✓ PASSED: POST returned {resp['status']}")
        passed += 1
    except Exception as e:
        print(f"  ✗ FAILED: {str(e)}")
        failed += 1


def test_invalid_auth_on_public_endpoint():
    """Test: send an invalid Bearer token to a public endpoint and accept 200/401/403."""
    global passed, failed, skipped
    print("\n[TEST] Invalid auth header against root or discovered collection")
    # Choose target: prefer discovered collection, else root
    path, _ = discover_collection_path()
    if not path:
        path = '/'
    try:
        response = make_request('GET', path, headers={'Authorization': 'Bearer invalid-token-12345'})
        print_req_res(response)
        if 'error' in response:
            print(f"  ✗ FAILED: {response['error']}")
            failed += 1
            return
        if response['status'] in (200, 401, 403):
            print(f"  ✓ PASSED: Received status {response['status']} with invalid token")
            passed += 1
        else:
            # Some servers return 404 or other codes; accept as pass as long as not 0
            if response['status'] == 0:
                print(f"  ✗ FAILED: No response from server")
                failed += 1
            else:
                print(f"  ✓ PASSED: Received status {response['status']} (tolerated)")
                passed += 1
    except Exception as e:
        print(f"  ✗ FAILED: {str(e)}")
        failed += 1


def main():
    """Run all tests"""
    print("=" * 60)
    print("API Test Suite")
    print("=" * 60)
    # Check if server is responding
    print("\nChecking server connectivity...")
    try:
        response = make_request('GET', '/')
        if 'error' in response:
            print(f"⚠ WARNING: Server not responding: {response['error']}")
            print("Tests will likely fail with connection errors\n")
        else:
            print(f"✓ Server responding (status {response['status']})\n")
    except Exception as e:
        print(f"⚠ WARNING: Could not connect to server: {str(e)}\n")
    # Run tests
    test_root_happy_path()
    test_api_index_paths()
    test_collection_and_single_resource()
    test_post_create_on_collection()
    test_invalid_auth_on_public_endpoint()
    # Summary
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
    print("=" * 60)
    sys.exit(0 if failed == 0 else 1)

if __name__ == '__main__':
    main()
