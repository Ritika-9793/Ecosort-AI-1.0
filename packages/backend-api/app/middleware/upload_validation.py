import io
from fastapi import UploadFile, HTTPException, status
from PIL import Image
from app.core.config import settings


async def validate_image_upload(file: UploadFile) -> bytes:
    """
    3-Tier File Upload Security Validator:
    1. Check maximum file size (5MB).
    2. Validate MIME type against allowed list.
    3. Re-encode image via PIL to strip EXIF & malicious payloads.
    """
    # 1. Size Check
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)}MB."
        )

    # 2. Content Type Check
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type '{file.content_type}'. Allowed types: {', '.join(settings.ALLOWED_MIME_TYPES)}"
        )

    # 3. PIL Integrity Re-encoding Check
    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()  # Verify image header integrity
        
        # Re-open after verify() (PIL requirement)
        image = Image.open(io.BytesIO(contents))
        output_buffer = io.BytesIO()
        image.save(output_buffer, format=image.format or "JPEG")
        sanitized_bytes = output_buffer.getvalue()
        return sanitized_bytes
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is corrupted or not a valid image format."
        )
