## **Technologies Used**

### **Backend (API)**

* **Framework:** FastAPI (Python)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy

### **Frontend (UI)**

* **Library:** React
* **Language:** TypeScript
* **Styling:** Tailwind CSS / Shadcn

---

## **Getting Started**

### **1. Setup the Backend**

1. **Clone the repository:**

   ```bash
   git clone [Your Repository URL]
   cd [Your Backend Directory, e.g., backend]
   ```
2. **Create a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Configure environment variables:**
   Create a file named `.env` in the backend directory and add your database configuration:

   ```
   # Example .env file content
   DATABASE_URL="postgresql://user:password@host:port/dbname"
   SECRET_KEY="your-fastapi-secret"
   ```

4. **Start the server:**

   ```bash
   uvicorn app.main:app --reload
   ```

   The API should now be running at `http://127.0.0.1:8000`.

### **2. Setup the Frontend**

1. **Navigate to the frontend directory:**

   ```bash
   cd ui
   ```
2. **Install dependencies:**

   ```bash
   npm install  # or yarn install
   ```
3. **Start the React development server:**

   ```bash
   npm start  # or yarn start
   ```
   The React application should open in your browser at `http://localhost:3000`.
