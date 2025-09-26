
# 🌴 Palm Minds Backend Task

This repository contains the backend implementation for the **Palm Minds hiring task**.

## ✨ Features

### 📄 Document Ingestion API

* Upload `.pdf` and `.txt` files
* Extract text and apply chunking strategies
* Generate embeddings and store them in **Qdrant**
* Save file metadata in **MySQL**

### 💬 Conversational RAG API

* Custom **RAG pipeline** (without `RetrievalQAChain`)
* **Redis** for chat memory
* Multi-turn query support
* Interview booking (name, email, date, time) stored in **MySQL**

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

Make sure you have the following installed:

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/)

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

---

### 3️⃣ Configure Environment Variables

Create a `.env` file in the project root with the following content:

```env
# Database
DATABASE_DSN=mysql+pymysql://root:${MYSQL_ROOT_PASSWORD}@mysql:3306/${MYSQL_DATABASE}
MYSQL_ROOT_PASSWORD=your_mysql_password
MYSQL_DATABASE=palm_minds

# Redis
REDIS_URL=redis://redis:6379/0

# Qdrant
QDRANT_URL=http://qdrant:6333
QDRANT_API_KEY=your_qdrant_api_key

# Embeddings
EMBEDDING_API_KEY=your_embedding_api_key
```

---

### 4️⃣ Start the Services

```bash
docker-compose up -d --build
```

---

### 5️⃣ Check API Logs

```bash
docker-compose logs -f api
```

---

### 6️⃣ Stop the Services

```bash
docker-compose down
```

---

## 🛠 Tech Stack

* **FastAPI** – API framework
* **MySQL** – Metadata storage
* **Qdrant** – Vector database for embeddings
* **Redis** – Chat memory storage
* **Docker & Docker Compose** – Containerization

---

## 📌 Notes

* Ensure `.env` is correctly configured before running services.
* Replace placeholder values (`your_mysql_password`, `your_embedding_api_key`, etc.) with actual credentials.

---

