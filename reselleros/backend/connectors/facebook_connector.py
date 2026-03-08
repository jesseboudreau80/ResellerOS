
def authenticate():
    return {"provider": "facebook", "status": "ok"}


def create_listing(item):
    return {
        "listing_id": f"FB-{item.sku}",
        "url": f"https://example.facebook.com/{item.sku}",
    }


def update_listing(item):
    return {"status": "updated", "sku": item.sku}


def end_listing(item):
    return {"status": "ended", "sku": item.sku}
