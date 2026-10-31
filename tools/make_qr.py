"""QR code to the open-access page of Sound Actions at MIT Press. Writes images/qr-sound-actions.svg.
Run from reveal/ with .venv/bin/python."""
import qrcode
import qrcode.image.svg

URL = "https://direct.mit.edu/books/oa-monograph/5513/Sound-ActionsConceptualizing-Musical-Instruments"
qrcode.make(URL, image_factory=qrcode.image.svg.SvgPathFillImage, border=2).save("images/qr-sound-actions.svg")
print("wrote images/qr-sound-actions.svg")
