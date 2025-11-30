import io

from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
import qrcode

from app.models.url import UrlCreate


router = APIRouter(prefix="/qr", tags=["QR Generator"])

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)


@router.post(
    "/generate",
    status_code=201,
    response_class=Response,
    responses={201: {"content": {"image/jpeg": {}}}},
)
async def generate(payload: UrlCreate):
    qr.add_data(payload.url)
    qr.make(fit=True)
    bytes = io.BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(bytes, format="JPEG")
    bytes.seek(0)
    qr.clear()
    return StreamingResponse(bytes, media_type="image/jpeg")
