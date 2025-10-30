# CSP Agent

This is a Python-based CSP Agent designed to interact with external systems via APIs.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/statstream/csp-agent.git
cd csp-agent
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install google-adk

```bash
pip install google-adk
```

### 4. Run agent

```bash
adk api_server --host=0.0.0.0 --port=8000
```
