from model import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE() AS database_name, VERSION() AS version")
    result = cursor.fetchone()

    print("✅ Koneksi TiDB berhasil!")
    print("Database:", result["database_name"])
    print("Version:", result["version"])

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Koneksi TiDB gagal!")
    print("Error:", e)
