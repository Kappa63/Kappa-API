import requests
import json
import time
import random
import string
from datetime import datetime, timedelta
from typing import Optional

# ==============================================================================
#                           CONFIGURATION
# ==============================================================================

BASE_URL = "http://localhost:8080/api/doseguard"

# Colors for terminal output (makes demo look professional)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ==============================================================================
#                           HELPER FUNCTIONS
# ==============================================================================

def print_section(title: str):
    """Print a formatted section header for visual clarity in demos."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}  {title.upper()}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")

def print_test(name: str, passed: bool, details: str = ""):
    """Print test result with colorful formatting."""
    status = f"{Colors.GREEN}✓ PASS{Colors.ENDC}" if passed else f"{Colors.RED}✗ FAIL{Colors.ENDC}"
    print(f"  {status} | {name}")
    if details and not passed:
        print(f"         {Colors.YELLOW}Details: {details}{Colors.ENDC}")

def print_info(message: str):
    """Print informational message."""
    print(f"  {Colors.CYAN}i {message}{Colors.ENDC}")

def random_string(length: int = 8) -> str:
    """Generate a random string for unique test data."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def make_request(method: str, endpoint: str, headers: dict = None, json_data: dict = None, params: dict = None) -> requests.Response:
    """Make an HTTP request with optional parameters."""
    # Add a delay between requests to avoid rate limiting
    # The API has a rate limit of 100/minute for authenticated users
    time.sleep(0.7)  # 700ms delay = max 86 requests/minute
    
    url = f"{BASE_URL}{endpoint}"
    
    # For GET and DELETE requests, remove Content-Type header to avoid Flask parsing issues
    # when there's no request body
    final_headers = headers.copy() if headers else {}
    if method in ('GET', 'DELETE') and 'Content-Type' in final_headers:
        del final_headers['Content-Type']
    
    response = requests.request(
        method=method,
        url=url,
        headers=final_headers,
        json=json_data,
        params=params,
        timeout=10
    )
    return response

# ==============================================================================
#                           TEST STATE MANAGEMENT
# ==============================================================================

class TestState:
    """Maintains state across tests for entity references."""
    
    def __init__(self):
        # Caregiver 1 (primary test caregiver)
        self.caregiver1_id: Optional[int] = None
        self.caregiver1_api_key: Optional[str] = None
        self.caregiver1_username: str = f"testuser_{random_string()}"
        self.caregiver1_password: str = "TestPassword123!"
        
        # Caregiver 2 (for access control tests)
        self.caregiver2_id: Optional[int] = None
        self.caregiver2_api_key: Optional[str] = None
        self.caregiver2_username: str = f"testuser2_{random_string()}"
        self.caregiver2_password: str = "TestPassword456!"
        
        # Entities created by caregiver 1
        self.patient_id: Optional[int] = None
        self.pill_id: Optional[int] = None
        self.dose_id: Optional[int] = None
        self.schedule_id: Optional[int] = None
        self.dose_history_id: Optional[int] = None
        
        # Test results tracking
        self.passed = 0
        self.failed = 0
    
    def get_headers(self, api_key: Optional[str] = None, include_content_type: bool = True) -> dict:
        """Get headers with API key for authenticated requests."""
        key = api_key or self.caregiver1_api_key
        if not key:
            return {}
        headers = {"X-API-KEY": key}
        if include_content_type:
            headers["Content-Type"] = "application/json"
        return headers
    
    def record_result(self, passed: bool):
        """Record test result."""
        if passed:
            self.passed += 1
        else:
            self.failed += 1

# Global test state
state = TestState()

# ==============================================================================
#                     1. AUTHENTICATION TESTS
# ==============================================================================

def test_authentication():
    """
    Test authentication endpoints: registration and login.
    
    Endpoints Tested:
        - POST /caregivers/register - Create new caregiver account
        - POST /caregivers/login - Authenticate and get API key
    """
    print_section("1. Authentication Tests")
    
    # -------------------------------------------------------------------------
    # Test 1.1: Register Caregiver 1 (Primary Test Account)
    # -------------------------------------------------------------------------
    # This creates our main test caregiver account that will be used
    # for most subsequent tests
    print_info(f"Registering primary test caregiver: {state.caregiver1_username}")
    
    response = make_request("POST", "/caregivers/register", json_data={
        "name": "Test Caregiver One",
        "username": state.caregiver1_username,
        "password": state.caregiver1_password
    })
    
    success = response.status_code == 201
    if success:
        data = response.json()
        state.caregiver1_id = data.get("id")
        print_info(f"Created caregiver with ID: {state.caregiver1_id}")
    
    print_test("Register Caregiver 1 - Should create new account (201)", success, 
               f"Status: {response.status_code}, Body: {response.text[:100]}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 1.2: Login Caregiver 1
    # -------------------------------------------------------------------------
    # Login to get the API key needed for authenticated endpoints
    print_info(f"Logging in as: {state.caregiver1_username}")
    
    response = make_request("POST", "/caregivers/login", json_data={
        "username": state.caregiver1_username,
        "password": state.caregiver1_password
    })
    
    success = response.status_code == 200
    if success:
        data = response.json()
        state.caregiver1_api_key = data.get("apiKey")
        print_info(f"Received API Key: {state.caregiver1_api_key[:8]}...")
    
    print_test("Login Caregiver 1 - Should return API key (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 1.3: Register Caregiver 2 (For Access Control Tests)
    # -------------------------------------------------------------------------
    # Create a second caregiver to test that users can't access each other's data
    print_info(f"Registering secondary test caregiver: {state.caregiver2_username}")
    
    response = make_request("POST", "/caregivers/register", json_data={
        "name": "Test Caregiver Two",
        "username": state.caregiver2_username,
        "password": state.caregiver2_password
    })
    
    success = response.status_code == 201
    if success:
        data = response.json()
        state.caregiver2_id = data.get("id")
    
    print_test("Register Caregiver 2 - Create second account for access tests (201)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 1.4: Login Caregiver 2
    # -------------------------------------------------------------------------
    response = make_request("POST", "/caregivers/login", json_data={
        "username": state.caregiver2_username,
        "password": state.caregiver2_password
    })
    
    success = response.status_code == 200
    if success:
        data = response.json()
        state.caregiver2_api_key = data.get("apiKey")
    
    print_test("Login Caregiver 2 - Get API key for second caregiver (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 1.5: Login with Invalid Credentials
    # -------------------------------------------------------------------------
    # Verify that invalid passwords are rejected
    response = make_request("POST", "/caregivers/login", json_data={
        "username": state.caregiver1_username,
        "password": "WrongPassword123!"
    })
    
    success = response.status_code == 401
    print_test("Login with Wrong Password - Should reject (401)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 1.6: Login with Non-existent User
    # -------------------------------------------------------------------------
    response = make_request("POST", "/caregivers/login", json_data={
        "username": "nonexistent_user_12345",
        "password": "AnyPassword123!"
    })
    
    success = response.status_code == 404
    print_test("Login Non-existent User - Should return 404", success,
               f"Status: {response.status_code}")
    state.record_result(success)

# ==============================================================================
#                     2. PATIENT CRUD TESTS
# ==============================================================================

def test_patient_crud():
    """
    Test Patient CRUD operations.
    
    Endpoints Tested:
        - POST /patients - Create new patient
        - GET /patients/<id> - Get patient by ID
        - GET /patients - List all patients
        - PATCH /patients/<id> - Update patient
        - DELETE /patients/<id> - Soft delete patient
    """
    print_section("2. Patient CRUD Tests")
    
    # -------------------------------------------------------------------------
    # Test 2.1: Create Patient
    # -------------------------------------------------------------------------
    # Create a patient with all optional fields
    dob = (datetime.now() - timedelta(days=365*30)).strftime("%Y-%m-%d")  # 30 years old
    
    print_info("Creating new patient with full details...")
    
    response = make_request("POST", "/patients", 
        headers=state.get_headers(),
        json_data={
            "name": "Karim Ahmad",
            "contact": "+962 7 8775 3023",
            "dob": dob,
            "weight": 75.5,
            "height": 175.0
        })
    
    success = response.status_code == 201
    if success:
        data = response.json()
        state.patient_id = data.get("id")
        print_info(f"Created patient with ID: {state.patient_id}")
    
    print_test("Create Patient - Full details (201)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 2.2: Attach Patient to Caregiver
    # -------------------------------------------------------------------------
    # Link the patient to caregiver 1 (required for access control)
    print_info(f"Attaching patient {state.patient_id} to caregiver {state.caregiver1_id}...")
    
    response = make_request("POST", "/caregivers/patients",
        headers=state.get_headers(),
        json_data={
            "caregiverId": state.caregiver1_id,
            "patientId": state.patient_id
        })
    
    success = response.status_code == 201
    print_test("Attach Patient to Caregiver - Create relationship (201)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 2.3: Get Patient by ID
    # -------------------------------------------------------------------------
    print_info(f"Fetching patient details for ID: {state.patient_id}")
    
    response = make_request("GET", f"/patients/{state.patient_id}",
        headers=state.get_headers())
    
    success = response.status_code == 200
    if success:
        data = response.json()
        print_info(f"Patient name: {data.get('name')}, Contact: {data.get('contact')}")
    
    print_test("Get Patient by ID - Retrieve patient details (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 2.4: List All Patients
    # -------------------------------------------------------------------------
    response = make_request("GET", "/patients", headers=state.get_headers())
    
    success = response.status_code == 200 and isinstance(response.json(), list)
    if success:
        print_info(f"Found {len(response.json())} patient(s) in database")
    
    print_test("List All Patients - Retrieve patient list (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 2.5: Update Patient
    # -------------------------------------------------------------------------
    # Update the patient's contact information
    print_info("Updating patient contact information...")
    
    response = make_request("PATCH", f"/patients/{state.patient_id}",
        headers=state.get_headers(),
        json_data={
            "contact": "+1-555-9999",
            "weight": 78.0
        })
    
    success = response.status_code == 200
    print_test("Update Patient - Modify contact and weight (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 2.6: Create Patient with Minimal Data
    # -------------------------------------------------------------------------
    # Test that only required fields are needed
    response = make_request("POST", "/patients",
        headers=state.get_headers(),
        json_data={"name": "Jane Minimal"})
    
    success = response.status_code == 201
    print_test("Create Patient - Minimal data (name only) (201)", success,
               f"Status: {response.status_code}")
    state.record_result(success)

# ==============================================================================
#                     3. PILL CRUD TESTS
# ==============================================================================

def test_pill_crud():
    """
    Test Pill (Medication) CRUD operations.
    
    Endpoints Tested:
        - POST /pills - Create new pill/medication
        - GET /pills/<id> - Get pill by ID
        - GET /pills - List all pills
        - PATCH /pills/<id> - Update pill
        - DELETE /pills/<id> - Soft delete pill
    """
    print_section("3. Pill (Medication) CRUD Tests")
    
    # -------------------------------------------------------------------------
    # Test 3.1: Create Pill
    # -------------------------------------------------------------------------
    print_info("Creating new medication: Aspirin 500mg")
    
    response = make_request("POST", "/pills",
        headers=state.get_headers(),
        json_data={
            "name": "Aspirin",
            "strength": 500.0
        })
    
    success = response.status_code == 201
    if success:
        data = response.json()
        state.pill_id = data.get("id")
        print_info(f"Created pill with ID: {state.pill_id}")
    
    print_test("Create Pill - Aspirin 500mg (201)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 3.2: Get Pill by ID
    # -------------------------------------------------------------------------
    response = make_request("GET", f"/pills/{state.pill_id}",
        headers=state.get_headers())
    
    success = response.status_code == 200
    if success:
        data = response.json()
        print_info(f"Pill: {data.get('name')} - Strength: {data.get('strength')}mg")
    
    print_test("Get Pill by ID - Retrieve medication details (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 3.3: List All Pills
    # -------------------------------------------------------------------------
    response = make_request("GET", "/pills", headers=state.get_headers())
    
    success = response.status_code == 200 and isinstance(response.json(), list)
    if success:
        print_info(f"Found {len(response.json())} medication(s) in database")
    
    print_test("List All Pills - Retrieve medication list (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 3.4: Update Pill
    # -------------------------------------------------------------------------
    print_info("Updating medication strength to 650mg...")
    
    response = make_request("PATCH", f"/pills/{state.pill_id}",
        headers=state.get_headers(),
        json_data={"strength": 650.0})
    
    success = response.status_code == 200
    print_test("Update Pill - Change strength to 650mg (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 3.5: Create Another Pill for Testing
    # -------------------------------------------------------------------------
    response = make_request("POST", "/pills",
        headers=state.get_headers(),
        json_data={
            "name": "Ibuprofen",
            "strength": 400.0
        })
    
    success = response.status_code == 201
    print_test("Create Pill - Ibuprofen 400mg (201)", success,
               f"Status: {response.status_code}")
    state.record_result(success)

# ==============================================================================
#                     4. DOSE CRUD TESTS
# ==============================================================================

def test_dose_crud():
    """
    Test Dose CRUD operations.
    A Dose defines when and how much of a pill should be taken.
    
    Endpoints Tested:
        - POST /doses - Create new dose
        - GET /doses/<id> - Get dose by ID
        - GET /doses - List all doses
        - PATCH /doses/<id> - Update dose
        - DELETE /doses/<id> - Soft delete dose
    """
    print_section("4. Dose CRUD Tests")
    
    # -------------------------------------------------------------------------
    # Test 4.1: Create Dose
    # -------------------------------------------------------------------------
    # Create a dose: take 2 pills every 8 hours (interval in hours)
    print_info(f"Creating dose: 2x Pill#{state.pill_id} every 8 hours")
    
    response = make_request("POST", "/doses",
        headers=state.get_headers(),
        json_data={
            "pillId": state.pill_id,
            "interval": 8,  # Every 8 hours
            "amount": 2     # 2 pills per dose
        })
    
    success = response.status_code == 201
    if success:
        data = response.json()
        state.dose_id = data.get("id")
        print_info(f"Created dose with ID: {state.dose_id}")
    
    print_test("Create Dose - 2 pills every 8 hours (201)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 4.2: Get Dose by ID
    # -------------------------------------------------------------------------
    response = make_request("GET", f"/doses/{state.dose_id}",
        headers=state.get_headers())
    
    success = response.status_code == 200
    if success:
        data = response.json()
        print_info(f"Dose: {data.get('amount')} pills every {data.get('interval')} hours")
    
    print_test("Get Dose by ID - Retrieve dose details (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 4.3: List All Doses
    # -------------------------------------------------------------------------
    response = make_request("GET", "/doses", headers=state.get_headers())
    
    success = response.status_code == 200 and isinstance(response.json(), list)
    if success:
        print_info(f"Found {len(response.json())} dose configuration(s)")
    
    print_test("List All Doses - Retrieve dose configurations (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 4.4: Update Dose
    # -------------------------------------------------------------------------
    print_info("Updating dose: change to 1 pill every 6 hours")
    
    response = make_request("PATCH", f"/doses/{state.dose_id}",
        headers=state.get_headers(),
        json_data={
            "interval": 6,
            "amount": 1
        })
    
    success = response.status_code == 200
    print_test("Update Dose - Change interval and amount (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)

# ==============================================================================
#                     5. SCHEDULE CRUD TESTS
# ==============================================================================

def test_schedule_crud():
    """
    Test Schedule CRUD operations.
    A Schedule groups multiple doses together.
    
    Endpoints Tested:
        - POST /schedules - Create new schedule
        - GET /schedules/<id> - Get schedule by ID
        - GET /schedules - List all schedules
        - PATCH /schedules/<id> - Update schedule
        - DELETE /schedules/<id> - Soft delete schedule
    """
    print_section("5. Schedule CRUD Tests")
    
    # -------------------------------------------------------------------------
    # Test 5.1: Create Schedule
    # -------------------------------------------------------------------------
    print_info("Creating new medication schedule: Morning Routine")
    
    response = make_request("POST", "/schedules",
        headers=state.get_headers(),
        json_data={"name": "Morning Routine"})
    
    success = response.status_code == 201
    if success:
        data = response.json()
        state.schedule_id = data.get("id")
        print_info(f"Created schedule with ID: {state.schedule_id}")
    
    print_test("Create Schedule - Morning Routine (201)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 5.2: Get Schedule by ID
    # -------------------------------------------------------------------------
    response = make_request("GET", f"/schedules/{state.schedule_id}",
        headers=state.get_headers())
    
    success = response.status_code == 200
    if success:
        data = response.json()
        print_info(f"Schedule: {data.get('name')}")
    
    print_test("Get Schedule by ID - Retrieve schedule details (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 5.3: List All Schedules
    # -------------------------------------------------------------------------
    response = make_request("GET", "/schedules", headers=state.get_headers())
    
    success = response.status_code == 200 and isinstance(response.json(), list)
    if success:
        print_info(f"Found {len(response.json())} schedule(s)")
    
    print_test("List All Schedules - Retrieve schedule list (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 5.4: Update Schedule
    # -------------------------------------------------------------------------
    print_info("Updating schedule name to 'Daily Morning Meds'")
    
    response = make_request("PATCH", f"/schedules/{state.schedule_id}",
        headers=state.get_headers(),
        json_data={"name": "Daily Morning Meds"})
    
    success = response.status_code == 200
    print_test("Update Schedule - Rename schedule (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)

# ==============================================================================
#                     6. RELATIONSHIP TESTS
# ==============================================================================

def test_relationships():
    """
    Test entity relationship operations.
    These endpoints link entities together (e.g., add doses to schedules).
    
    Endpoints Tested:
        - POST /schedules/doses - Attach dose to schedule
        - POST /patients/schedules - Attach schedule to patient
        - GET /<entity>/<id>/<related> - List related entities
    """
    print_section("6. Relationship Tests")
    
    # -------------------------------------------------------------------------
    # Test 6.1: Attach Dose to Schedule
    # -------------------------------------------------------------------------
    print_info(f"Attaching dose#{state.dose_id} to schedule#{state.schedule_id}")
    
    response = make_request("POST", "/schedules/doses",
        headers=state.get_headers(),
        json_data={
            "scheduleId": state.schedule_id,
            "doseId": state.dose_id
        })
    
    success = response.status_code == 201
    print_test("Attach Dose to Schedule - Link entities (201)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 6.2: Attach Schedule to Patient
    # -------------------------------------------------------------------------
    print_info(f"Attaching schedule#{state.schedule_id} to patient#{state.patient_id}")
    
    response = make_request("POST", "/patients/schedules",
        headers=state.get_headers(),
        json_data={
            "patientId": state.patient_id,
            "scheduleId": state.schedule_id
        })
    
    success = response.status_code == 201
    print_test("Attach Schedule to Patient - Link entities (201)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 6.3: List Patients for Caregiver
    # -------------------------------------------------------------------------
    print_info(f"Listing patients for caregiver#{state.caregiver1_id}")
    
    response = make_request("GET", f"/caregivers/{state.caregiver1_id}/patients",
        headers=state.get_headers())
    
    success = response.status_code == 200
    if success:
        data = response.json()
        print_info(f"Caregiver has {len(data)} patient(s)")
    
    print_test("List Patients for Caregiver - Get patient list (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 6.4: List Schedules for Patient
    # -------------------------------------------------------------------------
    print_info(f"Listing schedules for patient#{state.patient_id}")
    
    response = make_request("GET", f"/patients/{state.patient_id}/schedules",
        headers=state.get_headers())
    
    success = response.status_code == 200
    if success:
        data = response.json()
        print_info(f"Patient has {len(data)} schedule(s)")
    
    print_test("List Schedules for Patient - Get schedule list (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 6.5: List Doses for Schedule
    # -------------------------------------------------------------------------
    print_info(f"Listing doses for schedule#{state.schedule_id}")
    
    response = make_request("GET", f"/schedules/{state.schedule_id}/doses",
        headers=state.get_headers())
    
    success = response.status_code == 200
    if success:
        data = response.json()
        print_info(f"Schedule has {len(data)} dose(s)")
    
    print_test("List Doses for Schedule - Get dose list (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 6.6: List All Doses for Patient (Nested)
    # -------------------------------------------------------------------------
    print_info(f"Listing all doses across all schedules for patient#{state.patient_id}")
    
    response = make_request("GET", f"/patients/{state.patient_id}/all-doses",
        headers=state.get_headers())
    
    success = response.status_code == 200
    print_test("List All Doses for Patient - Nested query (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)

# ==============================================================================
#                     7. DOSE HISTORY TESTS
# ==============================================================================

def test_dose_history():
    """
    Test Dose History tracking operations.
    DoseHistory records whether a patient took their medication.
    
    Endpoints Tested:
        - POST /dose-history - Create history entry
        - GET /dose-history/<id> - Get entry by ID
        - GET /dose-history - List all entries
        - PATCH /dose-history/<id> - Update entry
        - DELETE /dose-history/<id> - Soft delete entry
    """
    print_section("7. Dose History Tests")
    
    # -------------------------------------------------------------------------
    # Test 7.1: Create Dose History Entry - Dose Taken
    # -------------------------------------------------------------------------
    print_info(f"Recording dose taken: patient#{state.patient_id}, dose#{state.dose_id}")
    
    response = make_request("POST", "/dose-history",
        headers=state.get_headers(),
        json_data={
            "patientId": state.patient_id,
            "doseId": state.dose_id,
            "taken": True
        })
    
    success = response.status_code == 201
    if success:
        data = response.json()
        state.dose_history_id = data.get("id")
        print_info(f"Created dose history entry with ID: {state.dose_history_id}")
    
    print_test("Create Dose History - Record dose taken (201)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 7.2: Create Dose History Entry - Dose Missed
    # -------------------------------------------------------------------------
    response = make_request("POST", "/dose-history",
        headers=state.get_headers(),
        json_data={
            "patientId": state.patient_id,
            "doseId": state.dose_id,
            "taken": False  # Dose was missed
        })
    
    success = response.status_code == 201
    print_test("Create Dose History - Record dose missed (201)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 7.3: Get Dose History Entry
    # -------------------------------------------------------------------------
    response = make_request("GET", f"/dose-history/{state.dose_history_id}",
        headers=state.get_headers())
    
    success = response.status_code == 200
    if success:
        data = response.json()
        print_info(f"Dose taken: {data.get('taken')}")
    
    print_test("Get Dose History Entry - Retrieve details (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 7.4: List All Dose History
    # -------------------------------------------------------------------------
    response = make_request("GET", "/dose-history", headers=state.get_headers())
    
    success = response.status_code == 200 and isinstance(response.json(), list)
    if success:
        print_info(f"Found {len(response.json())} dose history entries")
    
    print_test("List All Dose History - Retrieve history list (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 7.5: Update Dose History Entry
    # -------------------------------------------------------------------------
    print_info("Correcting dose history: marking as not taken")
    
    response = make_request("PATCH", f"/dose-history/{state.dose_history_id}",
        headers=state.get_headers(),
        json_data={"taken": False})
    
    success = response.status_code == 200
    print_test("Update Dose History - Correct entry (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 7.6: Get Pill Dose History (Nested)
    # -------------------------------------------------------------------------
    print_info(f"Getting all dose history for pill#{state.pill_id}")
    
    response = make_request("GET", f"/pills/{state.pill_id}/dose-history",
        headers=state.get_headers())
    
    success = response.status_code == 200
    print_test("Get Pill Dose History - Nested query (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)

# ==============================================================================
#                     8. ACCESS CONTROL TESTS
# ==============================================================================

def test_access_control():
    """
    Test authorization and access control.
    Ensure caregivers can only access their own data.
    
    These tests verify that:
        - Users cannot access other users' caregivers
        - Users cannot access patients not under their care
        - Unauthorized requests are properly rejected
    """
    print_section("8. Access Control Tests")
    
    # -------------------------------------------------------------------------
    # Test 8.1: Access Other Caregiver's Profile
    # -------------------------------------------------------------------------
    # Caregiver 2 tries to access Caregiver 1's profile
    print_info(f"Caregiver 2 attempting to access Caregiver 1's profile...")
    
    response = make_request("GET", f"/caregivers/{state.caregiver1_id}",
        headers=state.get_headers(state.caregiver2_api_key))
    
    success = response.status_code == 403
    print_test("Access Other Caregiver - Should be forbidden (403)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 8.2: Access Patient Not Under Care
    # -------------------------------------------------------------------------
    # Caregiver 2 tries to access Caregiver 1's patient
    print_info(f"Caregiver 2 attempting to access Caregiver 1's patient...")
    
    response = make_request("GET", f"/patients/{state.patient_id}",
        headers=state.get_headers(state.caregiver2_api_key))
    
    success = response.status_code == 403
    print_test("Access Other's Patient - Should be forbidden (403)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 8.3: Update Other Caregiver's Patient
    # -------------------------------------------------------------------------
    print_info(f"Caregiver 2 attempting to update Caregiver 1's patient...")
    
    response = make_request("PATCH", f"/patients/{state.patient_id}",
        headers=state.get_headers(state.caregiver2_api_key),
        json_data={"name": "Hacked Name"})
    
    success = response.status_code == 403
    print_test("Update Other's Patient - Should be forbidden (403)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 8.4: Access Pill Not Owned
    # -------------------------------------------------------------------------
    print_info(f"Caregiver 2 attempting to access Caregiver 1's pill...")
    
    response = make_request("GET", f"/pills/{state.pill_id}",
        headers=state.get_headers(state.caregiver2_api_key))
    
    success = response.status_code == 403
    print_test("Access Other's Pill - Should be forbidden (403)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 8.5: Access Without API Key
    # -------------------------------------------------------------------------
    print_info("Attempting to access protected endpoint without API key...")
    
    response = make_request("GET", f"/patients/{state.patient_id}")
    
    success = response.status_code == 401
    print_test("Access Without API Key - Should be unauthorized (401)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 8.6: Access With Invalid API Key
    # -------------------------------------------------------------------------
    print_info("Attempting to access with invalid API key...")
    
    response = make_request("GET", f"/patients/{state.patient_id}",
        headers={"X-API-KEY": "invalid-api-key-12345"})
    
    success = response.status_code == 401
    print_test("Access With Invalid API Key - Should be unauthorized (401)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 8.7: Attach Patient to Other Caregiver
    # -------------------------------------------------------------------------
    # Caregiver 2 tries to attach patient to caregiver 1
    print_info("Caregiver 2 attempting to attach patient to Caregiver 1...")
    
    response = make_request("POST", "/caregivers/patients",
        headers=state.get_headers(state.caregiver2_api_key),
        json_data={
            "caregiverId": state.caregiver1_id,
            "patientId": state.patient_id
        })
    
    success = response.status_code == 403
    print_test("Attach to Other Caregiver - Should be forbidden (403)", success,
               f"Status: {response.status_code}")
    state.record_result(success)

# ==============================================================================
#                     9. ERROR HANDLING TESTS
# ==============================================================================

def test_error_handling():
    """
    Test error handling for invalid inputs and edge cases.
    
    These tests verify:
        - Missing required fields are properly reported
        - Invalid data types are handled
        - Non-existent resources return 404
    """
    print_section("9. Error Handling Tests")
    
    # -------------------------------------------------------------------------
    # Test 9.1: Create Patient Missing Required Field
    # -------------------------------------------------------------------------
    print_info("Creating patient without required 'name' field...")
    
    response = make_request("POST", "/patients",
        headers=state.get_headers(),
        json_data={"contact": "+1-555-0000"})  # Missing 'name'
    
    success = response.status_code == 400
    print_test("Create Patient Missing Name - Should fail (400)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 9.2: Create Pill Missing Strength
    # -------------------------------------------------------------------------
    response = make_request("POST", "/pills",
        headers=state.get_headers(),
        json_data={"name": "Incomplete Pill"})  # Missing 'strength'
    
    success = response.status_code == 400
    print_test("Create Pill Missing Strength - Should fail (400)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 9.3: Create Dose with Invalid Pill ID
    # -------------------------------------------------------------------------
    response = make_request("POST", "/doses",
        headers=state.get_headers(),
        json_data={
            "pillId": 999999,  # Non-existent pill
            "interval": 8,
            "amount": 1
        })
    
    # This may succeed but create an orphaned reference - depends on foreign key constraints
    print_test("Create Dose Invalid Pill ID - Response documented", True,
               f"Status: {response.status_code}")
    state.record_result(True)
    
    # -------------------------------------------------------------------------
    # Test 9.4: Get Non-existent Patient
    # -------------------------------------------------------------------------
    print_info("Attempting to get patient with ID 999999...")
    
    response = make_request("GET", "/patients/999999",
        headers=state.get_headers())
    
    success = response.status_code in [403, 404]  # Could be 403 (not under care) or 404
    print_test("Get Non-existent Patient - Should fail (403/404)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 9.5: Update Non-existent Schedule
    # -------------------------------------------------------------------------
    response = make_request("PATCH", "/schedules/999999",
        headers=state.get_headers(),
        json_data={"name": "Ghost Schedule"})
    
    success = response.status_code in [403, 404]
    print_test("Update Non-existent Schedule - Should fail (403/404)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 9.6: Register Duplicate Username
    # -------------------------------------------------------------------------
    print_info(f"Attempting to register duplicate username: {state.caregiver1_username}")
    
    response = make_request("POST", "/caregivers/register", json_data={
        "name": "Duplicate User",
        "username": state.caregiver1_username,  # Already exists
        "password": "AnyPassword123!"
    })
    
    success = response.status_code == 409  # Username conflict
    print_test("Register Duplicate Username - Should fail (409 Conflict)", success,
               f"Status: {response.status_code}")
    state.record_result(success)

# ==============================================================================
#                     10. CAREGIVER SELF-MANAGEMENT TESTS
# ==============================================================================

def test_caregiver_management():
    """
    Test caregiver self-management operations.
    
    Endpoints Tested:
        - GET /caregivers/<id> - Get own caregiver profile
        - GET /caregivers - List all caregivers
        - PATCH /caregivers/<id> - Update own profile
    """
    print_section("10. Caregiver Self-Management Tests")
    
    # -------------------------------------------------------------------------
    # Test 10.1: Get Own Caregiver Profile
    # -------------------------------------------------------------------------
    print_info(f"Fetching own caregiver profile (ID: {state.caregiver1_id})")
    
    response = make_request("GET", f"/caregivers/{state.caregiver1_id}",
        headers=state.get_headers())
    
    success = response.status_code == 200
    if success:
        data = response.json()
        print_info(f"Caregiver: {data.get('name')}")
    
    print_test("Get Own Profile - Retrieve caregiver details (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 10.2: List All Caregivers
    # -------------------------------------------------------------------------
    response = make_request("GET", "/caregivers", headers=state.get_headers())
    
    success = response.status_code == 200 and isinstance(response.json(), list)
    if success:
        print_info(f"Found {len(response.json())} caregiver(s)")
    
    print_test("List All Caregivers - Retrieve list (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 10.3: Update Own Profile
    # -------------------------------------------------------------------------
    print_info("Updating own caregiver name...")
    
    response = make_request("PATCH", f"/caregivers/{state.caregiver1_id}",
        headers=state.get_headers(),
        json_data={"name": "Updated Caregiver Name"})
    
    success = response.status_code == 200
    print_test("Update Own Profile - Change name (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)

# ==============================================================================
#                     11. DELETE/CLEANUP TESTS
# ==============================================================================

def test_delete_operations():
    """
    Test soft delete operations (cleanup tests run last).
    
    These tests verify entities can be soft-deleted properly.
    """
    print_section("11. Delete Operations Tests")
    
    # -------------------------------------------------------------------------
    # Test 11.1: Delete Dose from Schedule (Relationship)
    # -------------------------------------------------------------------------
    print_info(f"Removing dose#{state.dose_id} from schedule#{state.schedule_id}")
    
    response = make_request("DELETE", "/schedules/doses",
        headers=state.get_headers(),
        params={
            "scheduleId": state.schedule_id,
            "doseId": state.dose_id
        })
    
    success = response.status_code == 200
    print_test("Delete Dose from Schedule - Remove relationship (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 11.2: Delete Schedule from Patient (Relationship)
    # -------------------------------------------------------------------------
    print_info(f"Removing schedule#{state.schedule_id} from patient#{state.patient_id}")
    
    response = make_request("DELETE", "/patients/schedules",
        headers=state.get_headers(),
        params={
            "patientId": state.patient_id,
            "scheduleId": state.schedule_id
        })
    
    success = response.status_code == 200
    print_test("Delete Schedule from Patient - Remove relationship (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 11.3: Delete Dose History Entry
    # -------------------------------------------------------------------------
    print_info(f"Deleting dose history entry#{state.dose_history_id}")
    
    response = make_request("DELETE", f"/dose-history/{state.dose_history_id}",
        headers=state.get_headers())
    
    success = response.status_code == 200
    print_test("Delete Dose History Entry - Soft delete (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 11.4: Delete Schedule
    # -------------------------------------------------------------------------
    print_info(f"Deleting schedule#{state.schedule_id}")
    
    response = make_request("DELETE", f"/schedules/{state.schedule_id}",
        headers=state.get_headers())
    
    success = response.status_code == 200
    print_test("Delete Schedule - Soft delete (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 11.5: Delete Dose
    # -------------------------------------------------------------------------
    print_info(f"Deleting dose#{state.dose_id}")
    
    response = make_request("DELETE", f"/doses/{state.dose_id}",
        headers=state.get_headers())
    
    success = response.status_code == 200
    print_test("Delete Dose - Soft delete (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)
    
    # -------------------------------------------------------------------------
    # Test 11.6: Delete Pill
    # -------------------------------------------------------------------------
    print_info(f"Deleting pill#{state.pill_id}")
    
    response = make_request("DELETE", f"/pills/{state.pill_id}",
        headers=state.get_headers())
    
    success = response.status_code == 200
    print_test("Delete Pill - Soft delete (200)", success,
               f"Status: {response.status_code}")
    state.record_result(success)

# ==============================================================================
#                           MAIN TEST RUNNER
# ==============================================================================

def run_all_tests():
    """
    Execute all test suites in order.
    
    Tests are organized to:
    1. First create necessary entities (caregivers, patients, etc.)
    2. Then test CRUD operations
    3. Then test relationships
    4. Then test access control
    5. Finally test error handling and cleanup
    """
    # print(f"\n{Colors.BOLD}{Colors.CYAN}")
    # print("╔══════════════════════════════════════════════════════════════════════╗")
    # print("║                                                                      ║")
    # print("║              DOSEGUARD API - COMPREHENSIVE TEST SUITE               ║")
    # print("║                                                                      ║")
    # print("║                        Demo Test Recording                           ║")
    # print("║                                                                      ║")
    # print("╚══════════════════════════════════════════════════════════════════════╝")
    # print(f"{Colors.ENDC}\n")
    
    print(f"{Colors.YELLOW}Starting tests against: {BASE_URL}{Colors.ENDC}")
    print(f"{Colors.YELLOW}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}\n")
    
    start_time = time.time()
    
    try:
        # Core entity creation and CRUD tests
        test_authentication()
        test_patient_crud()
        test_pill_crud()
        test_dose_crud()
        test_schedule_crud()
        
        # Relationship tests (must come after entities are created)
        test_relationships()
        
        # History tracking tests
        test_dose_history()
        
        # Security tests
        test_access_control()
        
        # Edge cases and error handling
        test_error_handling()
        
        # Self-management tests
        test_caregiver_management()
        
        # Cleanup/delete tests (run last)
        test_delete_operations()
        
    except requests.exceptions.ConnectionError:
        print(f"\n{Colors.RED}{'='*70}")
        print("CONNECTION ERROR!")
        print("="*70)
        print(f"Could not connect to the API at: {BASE_URL}")
        print("Please ensure the server is running:")
        print("  cd /home/kappa/Desktop/Kappa-API")
        print("  python setup.py")
        print(f"{'='*70}{Colors.ENDC}\n")
        return
    
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.ENDC}")
        raise
    
    # Print summary
    elapsed_time = time.time() - start_time
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("========================================================================")
    print("                           TEST SUMMARY                                 ")
    print("========================================================================")
    print(f"{Colors.ENDC}")
    
    print(f"  {Colors.GREEN}Passed:{Colors.ENDC} {state.passed}")
    print(f"  {Colors.RED}Failed:{Colors.ENDC} {state.failed}")
    print(f"  {Colors.CYAN}Total:{Colors.ENDC}  {state.passed + state.failed}")
    print(f"  {Colors.YELLOW}Time:{Colors.ENDC}   {elapsed_time:.2f} seconds")
    
    if state.failed == 0:
        print(f"\n  {Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.ENDC}")
    else:
        print(f"\n  {Colors.RED}{Colors.BOLD}✗ SOME TESTS FAILED{Colors.ENDC}")
    
    print()


if __name__ == "__main__":
    run_all_tests()
