"""
update_listings.py
Fetches https://www.idxhome.com/featured/98967, parses the listings,
and rewrites marker blocks in three HTML files:
  1. buying/listings/index.html        — all listings (no limit)
  2. index.html                        — homepage, first 3 only
  3. buying/buying-strategy-guide/index.html — next 3 (listings 4-6, no homepage overlap)
"""

import re
import sys
import requests
from bs4 import BeautifulSoup

# ── Config ────────────────────────────────────────────────────────────────────
IDX_URL = "https://www.idxhome.com/featured/98967"

TARGETS = [
    {
        "file":    "buying/listings/index.html",
        "start":   "<!-- LISTINGS:START -->",
        "end":     "<!-- LISTINGS:END -->",
        "offset":  0,
        "limit":   None,
        "card_fn": "build_card_listings",
    },
    {
        "file":    "index.html",
        "start":   "<!-- LISTINGS:START -->",
        "end":     "<!-- LISTINGS:END -->",
        "offset":  0,
        "limit":   3,
        "card_fn": "build_card_home",
    },
    {
        "file":    "buying/buying-strategy-guide/index.html",
        "start":   "<!-- LISTINGS:START -->",
        "end":     "<!-- LISTINGS:END -->",
        "offset":  3,       # skip the 3 already shown on homepage
        "limit":   3,
        "card_fn": "build_card_home",
    },
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def badge_class(status):
    s = status.lower()
    if "contingent" in s: return "badge-contingent", "Contingent"
    if "pending"    in s: return "badge-contingent", "Pending"
    return "badge-active", "Active"

def fmt_price(raw):
    raw = re.sub(r"[^\d]", "", raw)
    return f"${int(raw):,}" if raw else "—"

def parse_baths(baths_raw):
    parts = [p.strip() for p in baths_raw.split("|") if p.strip()]
    if len(parts) == 2:
        full, half = int(parts[0]), int(parts[1])
        return str(full + 0.5) if half else str(full)
    return parts[0] if parts else "—"

def listing_type(l):
    block = (l.get("raw_block") or "").lower()
    if "commercial" in block:
        return "commercial", "Commercial"
    if "land" in block or (l["beds"] == "—" and l["sqft"] == "—" and not l["units"]):
        return "land", "Land"
    return "residential", "Residential"

# ── Fetch & parse ─────────────────────────────────────────────────────────────
def fetch_listings():
    try:
        r = requests.get(IDX_URL, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except Exception as e:
        print(f"ERROR fetching IDX page: {e}")
        sys.exit(1)

    soup = BeautifulSoup(r.text, "html.parser")
    listings = []
    seen = set()

    for link_el in soup.select("a[href*='/homes/98967']"):
        href = link_el["href"]
        if href in seen:
            continue
        seen.add(href)

        detail_url = href if href.startswith("http") else "https://www.idxhome.com" + href

        raw_addr = link_el.get_text(" ", strip=True)
        if not raw_addr or len(raw_addr) < 5:
            continue

        addr_parts = [p.strip() for p in raw_addr.split(",")]
        street   = addr_parts[0].title()
        city_st  = ", ".join(addr_parts[1:]) if len(addr_parts) > 1 else ""
        city     = addr_parts[1].strip().title() if len(addr_parts) > 1 else ""
        city_key = slugify(city)

        # Walk up to find container with price/details
        container = link_el
        for _ in range(6):
            container = container.parent
            if container is None:
                break
            ct = container.get_text(" ", strip=True)
            if "Beds:" in ct or "$" in ct:
                break
        if container is None:
            container = link_el.parent

        block = container.get_text(" ", strip=True)

        # Price
        price_match = re.search(r"\$([\d,]+)", block)
        price_raw   = price_match.group(1).replace(",", "") if price_match else "0"
        price_fmt   = f"${int(price_raw):,}" if price_raw != "0" else "—"

        # Status
        status_raw = "Active"
        if "Contingent" in block: status_raw = "Contingent"
        if "Pending"    in block: status_raw = "Pending"
        badge_cls, badge_label = badge_class(status_raw)

        # Beds / baths / sqft / acres / units
        beds  = re.search(r"Beds:\s*(\d+)", block)
        baths = re.search(r"Baths:\s*([\d\s|]+)", block)
        sqft  = re.search(r"Sq\.\s*Ft\.:\s*([\d,N/A]+)", block)
        acres = re.search(r"Lot Acres:\s*([\d.]+)", block)
        units = re.search(r"Number of Units:\s*(\d+)", block)

        beds_val  = beds.group(1)               if beds  else "—"
        baths_val = parse_baths(baths.group(1)) if baths else "—"
        sqft_raw  = sqft.group(1).replace(",","") if sqft else "—"
        sqft_fmt  = f"{int(sqft_raw):,}" if sqft_raw not in ("—","N/A") else "—"
        acres_val = acres.group(1) if acres else None
        units_val = units.group(1) if units else None

        # MLS number from URL
        mls_match = re.search(r"/(\d{7,9})$", href)
        mls_num   = mls_match.group(1) if mls_match else ""

        # Image
        img_el  = container.select_one("img[src*='mlsgrid']")
        img_src = img_el["src"] if img_el else ""

        listings.append({
            "street":      street,
            "city_st":     city_st,
            "city_key":    city_key,
            "price_raw":   price_raw,
            "price_fmt":   price_fmt,
            "beds":        beds_val,
            "baths":       baths_val,
            "sqft":        sqft_fmt,
            "acres":       acres_val,
            "units":       units_val,
            "status":      status_raw.lower(),
            "badge_cls":   badge_cls,
            "badge_label": badge_label,
            "img_src":     img_src,
            "detail_url":  detail_url,
            "mls_num":     mls_num,
            "raw_block":   block,
        })

    return listings

# ── Card builders ─────────────────────────────────────────────────────────────

def build_card_listings(l, position):
    """Card style for buying/listings/index.html"""
    img_tag = (
        f'<img src="{l["img_src"]}" alt="{l["street"]}, {l["city_st"]}" loading="lazy" />'
        if l["img_src"] else
        '<div style="width:100%;height:100%;background:#dce3e8;"></div>'
    )

    stats = []
    if l["beds"] != "—":
        stats.append(f'<div class="listing-stat"><span class="stat-value">{l["beds"]}</span><span class="stat-label">Beds</span></div>')
    if l["baths"] != "—":
        stats.append(f'<div class="listing-stat"><span class="stat-value">{l["baths"]}</span><span class="stat-label">Baths</span></div>')
    if l["sqft"] != "—":
        stats.append(f'<div class="listing-stat"><span class="stat-value">{l["sqft"]}</span><span class="stat-label">Sq Ft</span></div>')
    if l["acres"]:
        stats.append(f'<div class="listing-stat"><span class="stat-value">{l["acres"]}</span><span class="stat-label">Acres</span></div>')
    if l["units"]:
        stats.append(f'<div class="listing-stat"><span class="stat-value">{l["units"]}</span><span class="stat-label">Units</span></div>')

    return f"""
        <!-- {l["street"]} -->
        <article class="listing-card reveal" data-city="{l["city_key"]}" data-price="{l["price_raw"]}" data-beds="{l["beds"]}" data-status="{l["status"]}">
          <div class="listing-card-photo">
            {img_tag}
            <span class="listing-badge {l["badge_cls"]}">{l["badge_label"]}</span>
          </div>
          <div class="listing-card-body">
            <p class="listing-price">{l["price_fmt"]}</p>
            <p class="listing-address">{l["street"]}</p>
            <p class="listing-city">{l["city_st"]}</p>
            <div class="listing-stats">
              {"".join(stats)}
            </div>
          </div>
          <div class="listing-card-footer"><a href="{l["detail_url"]}" target="_blank" rel="noopener" class="listing-detail-btn">View Details</a></div>
        </article>"""


def build_card_home(l, position):
    """Card style for index.html and buying-strategy-guide — matches .listing-card / .listing-info homepage markup."""
    img_tag = (
        f'<img src="{l["img_src"]}" alt="{l["street"]}, {l["city_st"]}" loading="lazy" itemprop="image">'
        if l["img_src"] else
        '<div style="width:100%;height:100%;background:#dce3e8;"></div>'
    )

    ltype_key, ltype_label = listing_type(l)

    if ltype_key == "commercial":
        badge_cls_extra = " commercial"
        badge_text = "Commercial"
    elif ltype_key == "land":
        badge_cls_extra = " land"
        badge_text = "Land"
    elif l["status"] == "contingent":
        badge_cls_extra = ""
        badge_text = "Contingent"
    else:
        badge_cls_extra = ""
        badge_text = "Active"

    meta_items = []
    if l["beds"] != "—":
        meta_items.append(f'<span class="listing-meta-item"><strong itemprop="numberOfBedrooms">{l["beds"]}</strong> bd</span>')
    if l["baths"] != "—":
        meta_items.append(f'<span class="listing-meta-item"><strong>{l["baths"]}</strong> ba</span>')
    if l["sqft"] != "—":
        meta_items.append(f'<span class="listing-meta-item"><strong>{l["sqft"]}</strong> sqft</span>')
    if l["acres"]:
        meta_items.append(f'<span class="listing-meta-item"><strong>{l["acres"]}</strong> acres</span>')
    if l["units"]:
        meta_items.append(f'<span class="listing-meta-item"><strong>{l["units"]}</strong> units</span>')

    mls_tag = f'<span class="listing-type-tag">{ltype_label}{" · MLS #" + l["mls_num"] if l["mls_num"] else ""}</span>'

    # Parse city / state / zip from city_st
    city_parts = [p.strip() for p in l["city_st"].split(",")]
    city_name  = city_parts[0] if city_parts else ""
    state_zip  = city_parts[1].strip() if len(city_parts) > 1 else "IL"
    state_parts = state_zip.split()
    city_state = state_parts[0] if state_parts else "IL"
    zip_code   = state_parts[1] if len(state_parts) > 1 else ""
    zip_span   = f' <span itemprop="postalCode">{zip_code}</span>' if zip_code else ""

    return f"""
      <!-- {l["street"]} -->
      <a href="{l["detail_url"]}"
         class="listing-card" target="_blank" rel="noopener"
         aria-label="{l["street"]}, {l["city_st"]} — {l["price_fmt"]}"
         itemscope itemtype="https://schema.org/RealEstateListing" itemprop="itemListElement">
        <meta itemprop="position" content="{position}">
        <div class="listing-photo">
          {img_tag}
          <span class="listing-badge{badge_cls_extra}">{badge_text}</span>
        </div>
        <div class="listing-info">
          <span class="listing-price" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
            <span itemprop="price" content="{l["price_raw"]}">{l["price_fmt"]}</span>
            <meta itemprop="priceCurrency" content="USD">
            <meta itemprop="availability" content="https://schema.org/InStock">
          </span>
          <span class="listing-address" itemprop="name">{l["street"]}</span>
          <span class="listing-city" itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">
            <span itemprop="addressLocality">{city_name}</span>, <span itemprop="addressRegion">{city_state}</span>{zip_span}
          </span>
          <div class="listing-divider"></div>
          <div class="listing-meta">
            {"".join(meta_items)}
          </div>
          {mls_tag}
        </div>
      </a>"""

# ── Inject into HTML ──────────────────────────────────────────────────────────
CARD_FNS = {
    "build_card_listings": build_card_listings,
    "build_card_home":     build_card_home,
}

def inject(listings, target):
    html_file    = target["file"]
    start_marker = target["start"]
    end_marker   = target["end"]
    offset       = target.get("offset", 0)
    limit        = target["limit"]
    card_fn      = CARD_FNS[target["card_fn"]]

    try:
        with open(html_file, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"SKIP: {html_file} not found — skipping.")
        return

    if start_marker not in html or end_marker not in html:
        print(f"SKIP: markers not found in {html_file}.")
        return

    # Slice the listings window: start at offset, take up to limit
    sliced = listings[offset:]
    subset = sliced[:limit] if limit else sliced

    if not subset:
        print(f"WARN: No listings available for {html_file} at offset {offset} — skipping to avoid wiping cards.")
        return

    cards_html = "\n".join(card_fn(l, i + 1) for i, l in enumerate(subset))

    new_block = f"{start_marker}\n{cards_html}\n      {end_marker}"
    pattern   = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL
    )
    updated = pattern.sub(new_block, html)

    # Update schema numberOfItems
    updated = re.sub(
        r'(itemprop="numberOfItems"\s+content=")[^"]*(")',
        rf'\g<1>{len(subset)}\g<2>',
        updated
    )

    # Update listings count display on listings page
    if not limit:
        updated = re.sub(
            r'(<strong>)\d+(</strong>\s*listing)',
            rf'\g<1>{len(subset)}\g<2>',
            updated
        )

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"✓ Wrote {len(subset)} listing(s) to {html_file} (offset {offset})")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Fetching {IDX_URL} ...")
    listings = fetch_listings()

    if not listings:
        print("No listings parsed — aborting to avoid wiping existing cards.")
        sys.exit(0)

    print(f"Found {len(listings)} listing(s). Updating target files ...")
    for target in TARGETS:
        inject(listings, target)
