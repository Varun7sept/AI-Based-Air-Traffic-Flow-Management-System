# ✈️ AI-Based Air Traffic Flow Management System

A real-time **AI-powered flight monitoring system** that detects potential aircraft collisions using live data from the [OpenSky Network](https://opensky-network.org/).  
The system uses **Flask, Socket.IO, Leaflet.js, and R-Tree spatial indexing** to fetch flight positions, analyze possible near misses, and visualize them on an interactive map.

---

## 🚀 Features
- 🌍 **Real-time Flight Tracking** → Live aircraft data from OpenSky API  
- ⚠️ **Collision Detection** → Identifies aircraft within dangerous thresholds (2 km horizontally, 500 m vertically)  
- 🛰 **Time-to-Collision (Simplified)** → Marks aircraft pairs that are dangerously close  
- 📊 **Interactive Dashboard** → Displays map, collision warnings, and detailed flight info  
- 🔄 **Live Updates** → Automatic refresh every 15 seconds via Socket.IO  

---

## 🖼 Screenshots
### 🌍 Flight Map  
![Map Screenshot](<img width="1316" height="600" alt="screenshotsmap png" src="https://github.com/user-attachments/assets/15349807-183c-409f-81f1-e9094fc77478" />
)

### ⚠️ Collision Warnings  
![Collisions Screenshot](<img width="697" height="343" alt="screenshotscollisions png" src="https://github.com/user-attachments/assets/2941e269-8fb7-4772-83cc-083adb7024ec" />
)

### 📊 Flight Details Table  
![Details Screenshot](<img width="659" height="398" alt="screenshotshome png" src="https://github.com/user-attachments/assets/40ef9f6f-8c98-4411-823e-2cf16d02a5db" />
)

---

## 🏗 Tech Stack
- **Backend**: Flask, Flask-SocketIO, Requests, Rtree  
- **Frontend**: HTML, CSS, JavaScript, Leaflet.js, Socket.IO  
- **API**: OpenSky Network API  
- **Other**: Multithreading for continuous updates  

---

## 📂 Project Structure
AI-Based-Air-Traffic-Flow-Management-System/
│
├── backend.py # Flask + Socket.IO backend
├── requirements.txt # Python dependencies
├── README.md # Documentation
│
├── templates/
│ └── index.html # Frontend (map + tables, links CSS & JS)
│
├── static/
│ ├── style.css # Styling (was inline in HTML)
│ └── script.js # JavaScript (was inline in HTML)
│
└── screenshots/
├── map.png
├── collisions.png
└── home.png



---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/<your-username>/AI-Based-Air-Traffic-Flow-Management-System.git
cd AI-Based-Air-Traffic-Flow-Management-System
2. Create Virtual Environment (optional but recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
3. Install Dependencies
pip install -r requirements.txt
4. Run Application
python backend.py
5. Access in Browser
Go to:
http://127.0.0.1:5000
📐 System Workflow
Backend (Flask) fetches live flight data from OpenSky API

Positions are stored in an R-Tree index for fast nearest-neighbor lookup

Collision detection runs continuously in the background

Socket.IO pushes updates to the frontend every 15 seconds

Frontend (Leaflet.js) updates map markers, warnings, and tables

⚠️ Limitations
OpenSky API may return limited data without authentication

Collision prediction is simplified (straight-line velocity assumption)

Performance may slow if tracking too many aircraft at once

📌 Future Improvements
✅ Implement advanced AI/ML models for accurate collision prediction

✅ Add filtering by airline, altitude, or region

✅ Deploy on cloud (Heroku, AWS, or Render)

✅ Add notification/alert system for severe collisions

👨‍💻 Author
Your Name
📧 Contact: varunbanda03@gmail.com
🌐 GitHub: @Varun7sept
