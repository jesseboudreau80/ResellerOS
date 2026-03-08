
def authenticate():
    return {"provider": "ebay", "status": "ok"}


def create_listing(item):
    return {
        "listing_id": f"EBAY-{item.sku}",
        "url": f"https://example.ebay.com/{item.sku}",
    }


def update_listing(item):
    return {"status": "updated", "sku": item.sku}


def end_listing(item):
    return {"status": "ended", "sku": item.sku}
