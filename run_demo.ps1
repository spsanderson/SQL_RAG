$env:DB_TYPE='sqlite'
$env:DB_NAME='demo.db'
$env:RAG_PERSIST_DIRECTORY='./data/vector_db_demo'

Write-Host "Starting SQL RAG Demo Application..."
Write-Host "Database: $env:DB_NAME"
Write-Host "Type: $env:DB_TYPE"
Write-Host "----------------------------------------"

python src/main.py
