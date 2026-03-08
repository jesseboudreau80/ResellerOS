# ResellerOS

Warehouse-style inventory and marketplace automation platform for resellers.

## Run backend

```bash
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

Set `NEXT_PUBLIC_API_URL=http://localhost:8000`.

## Core modules

- inventory
- warehouse
- barcode
- qr
- labels
- marketplace
- queue
- activity_logs
- analytics
