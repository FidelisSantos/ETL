# ETL Docker Setup

This project is now containerized with Docker. Each component runs in its own container.

## Container Structure

### Databases
- **mysql_standard**: MySQL on port 3307
- **mysql_john_deere**: MySQL on port 3308  
- **mongodb**: MongoDB on port 27017
- **clickhouse**: ClickHouse on ports 8123 and 9000

### Applications
- **dashboard**: Streamlit Dashboard on port 8501
- **etl_extract**: Main ETL task (extract.py)
- **etl_extract_realtime**: Real-time ETL task (extract_realtime.py)

## How to use

### 1. Start all services
```bash
docker-compose up -d
```

### 2. Start only databases
```bash
docker-compose up -d mysql_standard mysql_john_deere mongodb clickhouse
```

### 3. Start only the dashboard
```bash
docker-compose up -d dashboard
```

### 4. Start only ETL tasks
```bash
# Main task
docker-compose up -d etl_extract

# Real-time task
docker-compose up -d etl_extract_realtime
```

### 5. View logs
```bash
# View logs from all services
docker-compose logs -f

# View logs from a specific service
docker-compose logs -f dashboard
docker-compose logs -f etl_extract
docker-compose logs -f etl_extract_realtime
```

### 6. Stop services
```bash
docker-compose down
```

## Access Points

- **Dashboard**: http://localhost:8501
- **MySQL Standard**: localhost:3307
- **MySQL John Deere**: localhost:3308
- **MongoDB**: localhost:27017
- **ClickHouse**: localhost:8123

## Environment Variables

Environment variables are configured in the `docker.env` file and are automatically loaded by the ETL task containers.

## Container Rebuild

If you make changes to the code, you'll need to rebuild the containers:

```bash
# Rebuild all containers
docker-compose build

# Rebuild only the dashboard
docker-compose build dashboard

# Rebuild only the ETL tasks
docker-compose build etl_extract etl_extract_realtime
```
