import sys

from backend.services import generate_barcode_image

if __name__ == "__main__":
    value = sys.argv[1]
    sku = sys.argv[2]
    print(generate_barcode_image(value, sku))
