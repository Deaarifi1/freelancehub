from fastapi import Request

class TenantMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            tenant_id = request.headers.get("X-Tenant-ID", None)
            scope["tenant_id"] = tenant_id
        
        await self.app(scope, receive, send)