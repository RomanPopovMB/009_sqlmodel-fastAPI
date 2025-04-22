import time
from fastapi import Request

async def log_requests(request: Request, call_next):
    start_time = time.time()

    logfile = open("log.txt", "a")
    
    # Leer el cuerpo de la solicitud si es POST o PUT
    if request.method in ["POST", "PUT"]:
        body = await request.body()
        logfile.write(f"Request Body: {body.decode('utf-8')}.\n")
    
    response = await call_next(request)
    process_time = time.time() - start_time
    match(response.status_code):
        case 200:
            logfile.write(f"INFO request: {request.method} {request.url} - Processed in {process_time:.4f}s.\n")
        case 400:
            logfile.write(f"WARN request: {request.method} {request.url} - Processed in {process_time:.4f}s.\n")
        case 500:
            logfile.write(f"ERRO request: {request.method} {request.url} - Processed in {process_time:.4f}s.\n")
    
    
    logfile.close()

    return response
