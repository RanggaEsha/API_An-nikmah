import psycopg2

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='annikmah',
    user='postgres',
    password='postgres'
)


