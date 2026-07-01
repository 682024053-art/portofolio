import cloudinary
import cloudinary.uploader
from config import Config

cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET,
    secure=True
)


def upload_to_cloudinary(file, folder="portfolio"):
    if not file or file.filename == "":
        return None

    result = cloudinary.uploader.upload(
        file,
        folder=folder,
        resource_type="image"
    )

    return {
        "url": result.get("secure_url"),
        "public_id": result.get("public_id")
    }


def delete_from_cloudinary(public_id):
    if not public_id:
        return

    try:
        cloudinary.uploader.destroy(public_id)
    except Exception as e:
        print("Cloudinary delete error:", e)
