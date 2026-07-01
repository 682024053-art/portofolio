from config import Config
import resend

try:
    print("RESEND_API_KEY:", "ADA" if Config.RESEND_API_KEY else "KOSONG")
    print("MAIL_FROM:", Config.MAIL_FROM)
    print("ADMIN_EMAIL:", Config.ADMIN_EMAIL)

    if not Config.RESEND_API_KEY:
        raise Exception("RESEND_API_KEY kosong di .env")

    if not Config.MAIL_FROM:
        raise Exception("MAIL_FROM kosong di .env")

    if not Config.ADMIN_EMAIL:
        raise Exception("ADMIN_EMAIL kosong di .env")

    resend.api_key = Config.RESEND_API_KEY

    response = resend.Emails.send({
        "from": Config.MAIL_FROM,
        "to": [Config.ADMIN_EMAIL],
        "subject": "Test Email dari Flask Portfolio",
        "html": """
            <h2>Testing Resend Berhasil</h2>
            <p>Email ini dikirim dari project Flask Portfolio.</p>
        """
    })

    print("✅ Email berhasil dikirim ke Resend")
    print("Response:", response)

except Exception as e:
    print("❌ Email gagal dikirim")
    print("Error:", e)