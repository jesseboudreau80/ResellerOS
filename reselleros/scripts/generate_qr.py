import sys

from backend.services import generate_qr_image

if __name__ == "__main__":
    sku = sys.argv[1]
    print(generate_qr_image(sku))
