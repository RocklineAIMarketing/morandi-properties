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

        # MLS number from URL — moved ABOVE the image lookup so the
        # image fallback can use it
        mls_match = re.search(r"/(\d{7,9})$", href)
        mls_num   = mls_match.group(1) if mls_match else ""

        # ── Image (FIXED) ──────────────────────────────────────────────
        # idxhome actually serves photos from mgrid.idxhome.com, e.g.:
        #   https://mgrid.idxhome.com/images/MRD12729857/<uuid>.jpeg
        # The old selector looked for "mlsgrid" in the src, which never
        # matches — that's why every card fell back to a gray box.
        img_el = container.select_one("img[src*='mgrid.idxhome.com']")

        # Fallback 1: match by MLS number in the path (MRD<mls_num>)
        if not img_el and mls_num:
            img_el = container.select_one(f"img[src*='MRD{mls_num}']")

        # Fallback 2: just grab the first <img> in the container
        if not img_el:
            img_el = container.find("img")

        img_src = img_el["src"] if img_el and img_el.get("src") else ""

        # Normalize size params so all cards request a consistent thumbnail
        if img_src and "width=" not in img_src:
            sep = "&" if "?" in img_src else "?"
            img_src = f"{img_src}{sep}width=800&height=800"
        # ──────────────────────────────────────────────────────────────

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
