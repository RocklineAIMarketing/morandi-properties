"""
update_listings.py
Fetches https://www.idxhome.com/featured/98967, parses the listings,
and rewrites the LISTINGS:START / LISTINGS:END block in the target HTML file.
"""

import re
import sys
import requests
from bs4 import BeautifulSoup

# ── Config ────────────────────────────────────────────────────────────────────
IDX_URL       = "https://www.idxhome.com/featured/98967"
HTML_FILE     = "buying/listings/index.html"   # path inside your repo — adjust if needed
START_MARKER  = "<!-- LISTINGS:START -->"
END_MARKER    = "<!-- LISTINGS:END -->"

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
    if "contingent" in s:  return "badge-contingent", "Contingent"
    if "pending"    in s:  return "badge-contingent", "Pending"
    if "new"        in s:  return "badge-new",        "New"
    return "badge-active", "Active"

def fmt_price(raw):
    raw = re.sub(r"[^\d]", "", raw)
    return f"${int(raw):,}" if raw else "—"

def parse_baths(baths_raw):
    """'2 | 1' → '3'  (full + half → display as e.g. 2.5)"""
    parts = [p.strip() for p in baths_raw.split("|") if p.strip()]
    if len(parts) == 2:
        full, half = int(parts[0]), int(parts[1])
        return str(full + 0.5) if half else str(full)
    return parts[0] if parts else "—"

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

    for item in soup.select("li[class*='listing'], div[class*='listing-item'], .idx-listing"):
        # ── address ──────────────────────────────────────────────────────────
        link_el = item.select_one("a[href*='/homes/']")
        if not link_el:
            continue
        detail_url = link_el["href"]
        if not detail_url.startswith("http"):
            detail_url = "https://www.idxhome.com" + detail_url

        full_address = link_el.get_text(strip=True)
        # Split "742 GRANTON Place, Frankfort, IL 60423"
        parts = [p.strip() for p in full_address.split(",")]
        street   = parts[0].title() if parts else full_address
        city_st  = ", ".join(parts[1:]).strip() if len(parts) > 1 else ""
        city     = parts[1].strip().title() if len(parts) > 1 else ""
        city_key = slugify(city)

        # ── image ─────────────────────────────────────────────────────────────
        img_el  = item.select_one("img[src*='mlsgrid']")
        img_src = img_el["src"] if img_el else ""

        # ── price + status ────────────────────────────────────────────────────
        price_el  = item.select_one("span, div, p")
        price_raw = ""
        status_raw = "Active"

        # Walk all text nodes for price/status
        for el in item.find_all(string=True):
            txt = el.strip()
            if txt.startswith("$"):
                price_raw = txt
            if "Contingent" in txt:
                status_raw = "Contingent"
            if "Pending" in txt:
                status_raw = "Pending"

        price_fmt = fmt_price(price_raw)
        badge_cls, badge_label = badge_class(status_raw)

        # ── beds / baths / sqft ───────────────────────────────────────────────
        text_block = item.get_text(" ", strip=True)
        beds  = re.search(r"Beds:\s*(\d+)",   text_block)
        baths = re.search(r"Baths:\s*([\d\s|]+)", text_block)
        sqft  = re.search(r"Sq\.\s*Ft\.:\s*([\d,]+)", text_block)

        beds_val  = beds.group(1)  if beds  else "—"
        baths_val = parse_baths(baths.group(1)) if baths else "—"
        sqft_val  = sqft.group(1).replace(",", "")  if sqft  else "—"
        sqft_fmt  = f"{int(sqft_val):,}" if sqft_val != "—" else "—"

        listings.append({
            "street":      street,
            "city_st":     city_st,
            "city_key":    city_key,
            "price_raw":   re.sub(r"[^\d]", "", price_raw) or "0",
            "price_fmt":   price_fmt,
            "beds":        beds_val,
            "baths":       baths_val,
            "sqft":        sqft_fmt,
            "status":      status_raw.lower(),
            "badge_cls":   badge_cls,
            "badge_label": badge_label,
            "img_src":     img_src,
            "detail_url":  detail_url,
        })

    return listings

# ── Fallback: parse the simpler flat structure idxhome actually renders ────────
def fetch_listings_flat():
    """
    idxhome renders a flat page — this parser targets the actual markup
    seen when fetching the page as a bot.
    """
    try:
        r = requests.get(IDX_URL, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except Exception as e:
        print(f"ERROR fetching IDX page: {e}")
        sys.exit(1)

    soup = BeautifulSoup(r.text, "html.parser")
    listings = []

    # Each listing appears as an <a> with href /homes/...
    seen = set()
    for link_el in soup.select("a[href*='/homes/98967']"):
        href = link_el["href"]
        if href in seen:
            continue
        seen.add(href)

        detail_url = href if href.startswith("http") else "https://www.idxhome.com" + href

        # The address is the link text (or nearby text)
        raw_addr = link_el.get_text(" ", strip=True)
        if not raw_addr or len(raw_addr) < 5:
            continue

        # Parse address parts
        addr_parts = [p.strip() for p in raw_addr.split(",")]
        street   = addr_parts[0].title()
        city_st  = ", ".join(addr_parts[1:]) if len(addr_parts) > 1 else ""
        city     = addr_parts[1].strip().title() if len(addr_parts) > 1 else ""
        city_key = slugify(city)

        # Walk up to find the parent container for this listing
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

        # Beds / baths / sqft
        beds  = re.search(r"Beds:\s*(\d+)", block)
        baths = re.search(r"Baths:\s*([\d\s|]+)", block)
        sqft  = re.search(r"Sq\.\s*Ft\.:\s*([\d,N/A]+)", block)

        beds_val  = beds.group(1)             if beds  else "—"
        baths_val = parse_baths(baths.group(1)) if baths else "—"
        sqft_raw  = sqft.group(1).replace(",","") if sqft else "—"
        sqft_fmt  = f"{int(sqft_raw):,}" if sqft_raw not in ("—","N/A") else "—"

        # Image — find nearest img with mlsgrid src
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
            "status":      status_raw.lower(),
            "badge_cls":   badge_cls,
            "badge_label": badge_label,
            "img_src":     img_src,
            "detail_url":  detail_url,
        })

    return listings

# ── Card HTML builder ─────────────────────────────────────────────────────────
def build_card(l):
    sqft_block = ""
    if l["sqft"] != "—":
        sqft_block = f"""
              <div class="listing-stat"><span class="stat-value">{l["sqft"]}</span><span class="stat-label">Sq Ft</span></div>"""

    baths_block = ""
    if l["baths"] != "—":
        baths_block = f"""
              <div class="listing-stat"><span class="stat-value">{l["baths"]}</span><span class="stat-label">Baths</span></div>"""

    beds_block = ""
    if l["beds"] != "—":
        beds_block = f"""
              <div class="listing-stat"><span class="stat-value">{l["beds"]}</span><span class="stat-label">Beds</span></div>"""

    img_tag = (
        f'<img src="{l["img_src"]}" alt="{l["street"]}, {l["city_st"]}" loading="lazy" />'
        if l["img_src"] else
        '<div style="width:100%;height:100%;background:#dce3e8;"></div>'
    )

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
            <div class="listing-stats">{beds_block}{baths_block}{sqft_block}
            </div>
          </div>
          <div class="listing-card-footer"><a href="{l["detail_url"]}" target="_blank" rel="noopener" class="listing-detail-btn">View Details</a></div>
        </article>"""

# ── Inject into HTML ──────────────────────────────────────────────────────────
def inject(listings):
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    if START_MARKER not in html or END_MARKER not in html:
        print(f"ERROR: markers not found in {HTML_FILE}")
        print(f"  Add  {START_MARKER}  and  {END_MARKER}  around your listings grid content.")
        sys.exit(1)

    cards_html = "\n".join(build_card(l) for l in listings)
    count      = len(listings)

    new_block = f"{START_MARKER}\n{cards_html}\n        {END_MARKER}"
    pattern   = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL
    )
    updated = pattern.sub(new_block, html)

    # Also update the static results count span if present
    updated = re.sub(
        r'(<strong>)\d+(</strong>\s*listing)',
        rf'\g<1>{count}\g<2>',
        updated
    )

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"✓ Wrote {count} listing(s) to {HTML_FILE}")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Fetching {IDX_URL} ...")
    listings = fetch_listings_flat()

    if not listings:
        print("No listings parsed — aborting to avoid wiping existing cards.")
        sys.exit(0)

    print(f"Found {len(listings)} listing(s). Injecting into {HTML_FILE} ...")
    inject(listings)
