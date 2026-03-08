📦 ResellerOS

🚀 Warehouse-style inventory + listing automation for resellers

ResellerOS is a mobile-friendly inventory and marketplace automation platform designed for resellers operating from storage units, thrift stores, or small warehouses.

Instead of spreadsheets and manual listing workflows, ResellerOS provides a scan-based warehouse system that connects physical inventory with online marketplaces.

The goal is simple:

Scan item → manage inventory → publish listing → track profit

ResellerOS turns a storage unit into a mini fulfillment warehouse.

🧭 Purpose

Most reseller tools focus only on listing automation.
ResellerOS focuses on the entire reseller workflow:

inventory intake

warehouse tracking

QR + barcode scanning

label printing

listing automation

profit tracking

It combines:

Warehouse inventory system
+
Marketplace listing automation
+
AI-ready listing generation
🧠 Core Features
📦 Inventory Management

Automatic SKU generation

Photo uploads

cost + price tracking

status tracking (available / listed / sold)

📱 Mobile Scanning

Use your phone camera to:

scan QR codes

scan barcodes

open item pages instantly

move inventory between shelves

🏷 Label Printing

Each item can generate labels containing:

SKU

barcode

QR code

title

price

Supported formats:

4×6 thermal labels

standard label sheets

single printable labels

🏬 Warehouse Shelf Tracking

Items are tracked using bin locations:

A1
A2
A3
B1
B2
B3

Example workflow:

scan item
↓
scan shelf
↓
inventory location updated
⚡ Quick Add Intake

Fast inventory intake for new items.

take photo
↓
SKU generated
↓
barcode generated
↓
QR generated
↓
label printed

Item details can be edited later.

🌐 Marketplace Automation

Architecture includes connectors for:

eBay

Facebook Marketplace

Mercari

Publishing flow:

scan item
↓
generate listing
↓
publish
↓
track listing link
📊 Dashboard & Analytics

Dashboard provides:

total inventory

items listed

items sold

inventory value

profit tracking

🧱 Architecture

ResellerOS is designed with modular services.

inventory
warehouse
barcode
qr
labels
marketplace
job_queue
activity_logs
analytics
🧰 Technologies Used

Backend

Python

FastAPI

SQLite

SQLAlchemy

Frontend

Next.js

React

TailwindCSS

Libraries

qrcode

python-barcode

pillow

uvicorn

📂 Project Structure
reselleros/

backend/
  main.py
  models.py
  database.py

routes/
  items.py
  warehouse.py
  marketplace.py
  qr.py
  barcode.py

connectors/
  ebay_connector.py
  facebook_connector.py
  mercari_connector.py

frontend/
  pages/
    dashboard.tsx
    inventory.tsx
    item/[sku].tsx
    add-item.tsx
    scan.tsx

uploads/
  items/

scripts/
  generate_qr.py
  generate_barcode.py
⚙️ Installation

Clone the repository

git clone https://github.com/yourusername/reselleros.git
cd reselleros

Install backend dependencies

pip install -r requirements.txt

Run the backend

uvicorn main:app --reload

Start the frontend

npm install
npm run dev
📱 Example Workflow
Adding Inventory
Quick Add
↓
Take photo
↓
SKU generated
↓
Print label
↓
Place item on shelf
Moving Inventory
Scan item
↓
Scan shelf
↓
Location updated
Selling an Item
Scan item
↓
Mark sold
↓
Listing automatically ended
🔐 License

This project is currently proprietary software.

Copyright (c) Jesse Boudreau

All rights reserved.

Unauthorized copying, modification,
distribution, or use of this software
without written permission is prohibited.
🧠 Future Roadmap

Planned enhancements:

AI item recognition

automatic pricing suggestions

bulk cross-listing

sales analytics

CSV import/export

multi-user warehouse mode

SaaS deployment

👤 Author

Jesse Boudreau
Builder of tools for the pet industry, compliance automation, and AI-driven operations.

⭐ Project Vision

ResellerOS aims to become:

The operating system for modern resellers

Connecting physical inventory, scanning workflows, and online marketplaces into one unified platform.
