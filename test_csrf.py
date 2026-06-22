import asyncio
from curl_cffi import requests
from request_phase import _create_session, _common_headers

def test():
    session = _create_session(proxy=None)
    
    # Hit homepage first
    print("GET /")
    resp0 = session.get("https://chatgpt.com/", headers=_common_headers("https://chatgpt.com/"))
    print("Homepage status:", resp0.status_code)
    for header, value in resp0.headers.items():
        if header.lower() == 'set-cookie' and 'csrf' in value.lower():
            print("  Found CSRF cookie on homepage:", value)
            
    print("\nGET /api/auth/csrf")
    resp1 = session.get("https://chatgpt.com/api/auth/csrf", headers=_common_headers("https://chatgpt.com/"))
    print("CSRF status:", resp1.status_code)
    for header, value in resp1.headers.items():
        if header.lower() == 'set-cookie' and 'csrf' in value.lower():
            print("  Found CSRF cookie on /api/auth/csrf:", value)

    print("\nCookies in session:")
    for c in session.cookies.jar:
        print(f"  {c.name} = {c.value}")

test()
