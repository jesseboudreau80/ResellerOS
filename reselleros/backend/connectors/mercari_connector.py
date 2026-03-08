
def authenticate():
    return {"provider": "mercari", "status": "ok"}


def create_listing(item):
    return {
        "listing_id": f"MERC-{item.sku}",
        "url": f"https://example.mercari.com/{item.sku}",
    }


def update_listing(item):
    return {"status": "updated", "sku": item.sku}


def end_listing(item):
    return {"status": "ended", "sku": item.sku}
