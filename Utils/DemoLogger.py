import time
import json
from functools import wraps
from flask import request, g
from datetime import datetime


# ==============================================================================
#                           ANSI COLOR CODES
# ==============================================================================

class Colors:
    """ANSI escape codes for terminal colors."""
    
    # Text styles
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright foreground colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


# ==============================================================================
#                           HELPER FUNCTIONS
# ==============================================================================

def get_method_badge(method: str) -> str:
    """
    Get a colorful badge for the HTTP method.
    
    Different methods get different colors for easy identification:
        - GET:    Blue (read operations)
        - POST:   Green (create operations)
        - PUT:    Yellow (full update)
        - PATCH:  Cyan (partial update)
        - DELETE: Red (delete operations)
    """
    method_colors = {
        'GET': (Colors.BG_BLUE, Colors.WHITE),
        'POST': (Colors.BG_GREEN, Colors.BLACK),
        'PUT': (Colors.BG_YELLOW, Colors.BLACK),
        'PATCH': (Colors.BG_CYAN, Colors.BLACK),
        'DELETE': (Colors.BG_RED, Colors.WHITE),
    }
    
    bg, fg = method_colors.get(method, (Colors.BG_WHITE, Colors.BLACK))
    padded_method = f" {method:6} "
    return f"{Colors.BOLD}{padded_method}{Colors.RESET}"


def get_status_color(status_code: int) -> str:
    """
    Get the appropriate color for a status code.
    
        - 2xx: Green (success)
        - 3xx: Cyan (redirect)
        - 4xx: Yellow (client error)
        - 5xx: Red (server error)
    """
    if 200 <= status_code < 300:
        return Colors.BRIGHT_GREEN
    elif 300 <= status_code < 400:
        return Colors.BRIGHT_CYAN
    elif 400 <= status_code < 500:
        return Colors.BRIGHT_YELLOW
    else:
        return Colors.BRIGHT_RED


def truncate_json(data: dict, max_length: int = 200) -> str:
    """Truncate JSON to a reasonable preview length."""
    try:
        json_str = json.dumps(data, default=str)
        if len(json_str) > max_length:
            return json_str[:max_length] + "..."
        return json_str
    except:
        return str(data)[:max_length]


def get_separator() -> str:
    """Get a visual separator line."""
    return f"{Colors.DIM}{'─' * 80}{Colors.RESET}"


def get_header_separator() -> str:
    """Get a header separator with current timestamp."""
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    line = "═" * 35
    return f"\n{Colors.BRIGHT_MAGENTA}{line} {timestamp} {line}{Colors.RESET}"


# ==============================================================================
#                       LOGGING FUNCTIONS
# ==============================================================================

def log_request():
    """
    Log incoming request details.
    
    Displays:
        - HTTP method (color-coded)
        - Request path
        - Query parameters (if any)
        - Selected headers
        - Request body preview (if JSON)
    """
    # Store start time for duration calculation
    g.request_start_time = time.time()
    
    # Header
    print(get_header_separator())
    
    # Method and path
    method_badge = get_method_badge(request.method)
    path = request.path
    
    print(f"\n{Colors.BOLD}INCOMING REQUEST{Colors.RESET}")
    print(f"  {method_badge}  {Colors.BRIGHT_WHITE}{path}{Colors.RESET}")
    
    # Query parameters
    if request.args:
        print(f"\n  {Colors.DIM}Query Parameters:{Colors.RESET}")
        for key, value in request.args.items():
            print(f"    {Colors.CYAN}{key}{Colors.RESET}: {value}")
    
    # Headers (show only relevant ones)
    print(f"\n  {Colors.DIM}Headers:{Colors.RESET}")
    
    # API Key (masked for security)
    api_key = request.headers.get('X-API-KEY')
    if api_key:
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "****"
        print(f"    {Colors.YELLOW}X-API-KEY{Colors.RESET}: {masked_key}")
    
    content_type = request.headers.get('Content-Type')
    if content_type:
        print(f"    {Colors.YELLOW}Content-Type{Colors.RESET}: {content_type}")
    
    # Request body (only for methods that have bodies)
    if request.method in ('POST', 'PUT', 'PATCH'):
        try:
            if request.is_json and request.json:
                print(f"\n  {Colors.DIM}Request Body:{Colors.RESET}")
                body_preview = truncate_json(request.json)
                print(f"    {Colors.GREEN}{body_preview}{Colors.RESET}")
        except Exception:
            pass  # Ignore JSON parsing errors
    
    print()


def log_response(response):
    """
    Log outgoing response details.
    
    Displays:
        - Status code (color-coded)
        - Response time
        - Response body preview
    """
    # Calculate duration
    duration = time.time() - getattr(g, 'request_start_time', time.time())
    duration_ms = duration * 1000
    
    # Status with color
    status_color = get_status_color(response.status_code)
    status_text = f"{status_color}{Colors.BOLD}{response.status_code} {response.status}{Colors.RESET}"
    
    print(f"  {Colors.BOLD}OUTGOING RESPONSE{Colors.RESET}")
    print(f"    Status: {status_text}")
    print(f"    {Colors.DIM}Time:{Colors.RESET} {duration_ms:.2f}ms")
    
    # Response body preview
    try:
        if response.content_type and 'json' in response.content_type:
            data = response.get_json()
            if data:
                print(f"\n    {Colors.DIM}Response Body:{Colors.RESET}")
                body_preview = truncate_json(data)
                print(f"    {Colors.CYAN}{body_preview}{Colors.RESET}")
    except:
        pass
    
    print(f"\n{get_separator()}")
    
    return response


# ==============================================================================
#                       INITIALIZATION
# ==============================================================================

def init_demo_logging(app):
    """
    Initialize demo logging middleware for a Flask application.
    
    This should be called after creating the Flask app:
    
        app = Flask(__name__)
        init_demo_logging(app)
    
    The middleware will automatically log all requests and responses
    with colorful, easy-to-read formatting.
    """
    # Print startup banner
    # print(f"\n{Colors.BRIGHT_MAGENTA}{'═' * 80}{Colors.RESET}")
    # print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}")
    # print("  ╔═══════════════════════════════════════════════════════════════════════╗")
    # print("  ║                                                                       ║")
    # print("  ║                    🔍 DEMO LOGGING ENABLED 🔍                         ║")
    # print("  ║                                                                       ║")
    # print("  ║   All API requests and responses will be logged with detailed        ║")
    # print("  ║   colorful output for demo/recording purposes.                       ║")
    # print("  ║                                                                       ║")
    # print("  ╚═══════════════════════════════════════════════════════════════════════╝")
    # print(f"{Colors.RESET}")
    # print(f"{Colors.BRIGHT_MAGENTA}{'═' * 80}{Colors.RESET}\n")
    
    # Register before_request handler
    @app.before_request
    def before_request_logging():
        """Log details before processing the request."""
        # Skip swagger/static endpoints
        if request.path.startswith('/swagger') or request.path.startswith('/static'):
            return
        if request.path.startswith('/apispec') or request.path.startswith('/flasgger'):
            return
        log_request()
    
    # Register after_request handler
    @app.after_request
    def after_request_logging(response):
        """Log details after processing the request."""
        # Skip swagger/static endpoints
        if request.path.startswith('/swagger') or request.path.startswith('/static'):
            return response
        if request.path.startswith('/apispec') or request.path.startswith('/flasgger'):
            return response
        return log_response(response)
    
    print(f"{Colors.GREEN}✓ Demo logging middleware registered successfully{Colors.RESET}\n")
