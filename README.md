# 🏠 AppInventarios – Real Estate Inventory Management SaaS

**Status:** Production Beta – Running on [Railway](https://railway.app/) with one active client, stable and bug-free so far.

## 📌 Overview
**AppInventarios** is a **SaaS web application** for real estate companies to manage property inventories for both acquisition (*captación*) and delivery (*entrega*) processes.  
Built with **Django 5.1.5**, **Python 3.13.6**, **PostgreSQL**, and deployed in a **Dockerized** environment on Railway with automated CI/CD.

Unlike static inventory systems, **AppInventarios** offers a **fully dynamic form configuration**: each agency can define what information to collect, how many environments a property has, and the items per environment — all with **digital signatures** and PDF generation.

---

## 🚀 Key Features
- **Dynamic Form Builder**  
  - Agencies define the fields for both acquisition and delivery forms.  
  - Delivery form supports adding unlimited environments and items.

- **Full Inventory Lifecycle**  
  - **Acquisition Inventory** – Property details from owner/apoderado with digital signature.  
  - **Delivery Inventory** – For rental or sale, with configurable environments and items, digital signature, and PDF export.

- **Digital Signatures**  
  - Built-in canvas signature capture for both processes.

- **Responsive Design**  
  - 100% Bootstrap 5 for consistent web & mobile experience.

- **PDF Document Generation**  
  - Professional templates for signed inventories.

- **Secure Workflow**  
  - All critical actions require POST requests and confirmation prompts.

---

## 🛠 Tech Stack
- **Backend:** Python 3.13.6, Django 5.1.5
- **Database:** PostgreSQL
- **Containerization:** Docker
- **Deployment:** Railway (CI/CD pipeline)
- **Frontend:** HTML, CSS (Bootstrap 5), JavaScript
- **Maps:** Leaflet.js with browser geolocation
- **PDF & Signatures:** SignaturePad, Django templates

---

## 📂 Main Models
- **Property** – Full property details, including GPS location.
- **Client** – Contact and management details.
- **PropertyClient** – Flexible relationship between client and property (owner, proxy, tenant).
- **AcquisitionForm** – Customizable, dynamic form with signature and PDF.
- **DeliveryForm** – Dynamic form for tenants, supports environments and items, signature, and PDF.
- **Agency** – Branding, legal data, and user relationships.
- **Environment / Item** – Detailed inventory structure per property.

---

## 📸 Screenshots
*(To be added)*  
Suggested: Dashboard view, form creation, signature capture, PDF output.

---

## ⚙️ Installation
```bash
# 1. Clone the repository
git clone https://github.com/hernanagudelodev/appInventarios.git
cd appInventarios

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Example: create a .env file and configure DATABASE_URL, SECRET_KEY, DEBUG, etc.

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver

```

---

## 📜 License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact
**Hernán Agudelo López**  
📧 hernanagudelodev@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/hernan-agudelo) | [GitHub](https://github.com/hernanagudelodev)
