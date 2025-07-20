# AddBudgetSystem
# AdServer Project

A Django application for managing advertisers, budgets, campaigns, dayparts, and spend events, with asynchronous processing using Celery.

---

## Table of Contents

- [Requirements](#requirements)
- [Setup and Running Locally](#setup-and-running-locally)
- [Data Models and Relationships](#data-models-and-relationships)
- [System Daily Workflow](#system-daily-workflow)
- [Assumptions & Simplifications](#assumptions--simplifications)

---

## Requirements

- Python 3.10+
- Django 4.x
- Celery 5.x
- Redis (for Celery broker)
- django-celery-beat (for periodic tasks)

Install all Python dependencies with:

```bash
pip install -r requirements.txt
```

---

## Setup and Running Locally

1. **Clone the repository**

    ```bash
    git clone <repo-url>
    cd adserver_project
    ```

2. **Install requirements**

    ```bash
    pip install -r requirements.txt
    ```

3. **Apply migrations**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Create a superuser (optional, for admin access)**

    ```bash
    python manage.py createsuperuser
    ```

5. **Start Redis (in a separate terminal, required for Celery)**

    ```bash
    redis-server
    ```

6. **Start Django development server**

    ```bash
    python manage.py runserver
    ```

7. **Start the Celery worker (in a new terminal):**

    ```bash
    celery -A adserver_project worker --loglevel=info
    ```

8. **Start Celery beat (for scheduled tasks):**

    ```bash
    celery -A adserver_project beat --loglevel=info
    ```

---

## Data Models and Relationships

- **Advertiser**
  - Represents an entity running campaigns.
  - Has many `Campaign`s.

- **Budget**
  - Represents a set amount of money an advertiser allocates.
  - Belongs to an `Advertiser`.
  - Can have multiple `Campaign`s.

- **Campaign**
  - Represents an advertising campaign.
  - Belongs to an `Advertiser` and a `Budget`.
  - Has many `SpendEvent`s and `Daypart`s.

- **Daypart**
  - Represents a specific time period in a campaign (for scheduling).
  - Belongs to a `Campaign`.

- **SpendEvent**
  - Represents a record of money spent in a campaign.
  - Belongs to a `Campaign`.

**Relationships Diagram:**

```
Advertiser (1) ----< (M) Campaign (1) ----< (M) SpendEvent
       |                          |
       |                          +----< (M) Daypart
       |
       +----< (M) Budget (1) ----< (M) Campaign
```

---

## System Daily Workflow

- **1. Budget and Campaign Management:**  
  Admins or users create `Advertiser`, `Budget`, and `Campaign` records via the web interface.
- **2. Dayparts and Spend Events:**  
  `Daypart`s are configured per campaign for scheduling; `SpendEvent`s are created to log spend.
- **3. Celery Periodic Tasks:**  
  Celery Beat schedules daily or hourly tasks (e.g., spend capping, campaign status updates).
- **4. Spend Simulation (optional):**  
  Use a management command or admin to generate `SpendEvent`s for testing.
- **5. Monitoring:**  
  The web UI provides lists and details for all models.

---

## Assumptions & Simplifications

- **Authentication:**  
  Assumes only admin/superuser interaction for data entry; no custom user roles.
- **Simplified Budgeting:**  
  Budgets are not enforced at the database level; overspending must be handled in business logic.
- **Celery Broker:**  
  Redis is used as the Celery broker for simplicity.
- **No Real-Time Bidding:**  
  The system does not include actual ad delivery or bidding logic—just the management backend.
- **Minimal Frontend Styling:**  
  UI uses basic HTML/CSS, no JavaScript frameworks.
- **Error Handling:**  
  Simplified error handling for brevity in views and tasks.

---

## Questions?

For further questions, open an issue or contact the maintainer.

