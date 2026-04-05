# morandi-properties

**************Header and Footer Start Guide 
************** <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Morandi Properties</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600&family=Barlow:wght@300;400;500;600&display=swap" rel="stylesheet">

  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --white:      #ffffff;
      --blue-grey:  #b0bec5;
      --light-bg:   #f4f6f8;
      --navy:       #1a2d4a;
      --navy-light: #2e4a6e;
      --text-muted: #607d8b;
    }

    body { font-family: 'Barlow', sans-serif; color: var(--navy); }

    /* ─── HEADER ─────────────────────────────────────────────── */
    .site-header { width: 100%; background: linear-gradient(to bottom, #cfd8dc 0%, #b0bec5 100%); background-size: cover; background-position: center; }
    .logo-row { display: flex; justify-content: center; align-items: center; padding: 24px 40px 16px; }
    .logo-placeholder { font-family: 'Barlow Condensed', sans-serif; font-size: 28px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--navy); text-decoration: none; }
    .nav-row { display: flex; justify-content: center; align-items: center; padding: 0 40px 18px; border-top: 1px solid rgba(26,45,74,0.18); gap: 2px; }
    .nav-link { font-size: 12.5px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: var(--navy); text-decoration: none; padding: 12px 15px; white-space: nowrap; transition: color 0.2s; }
    .nav-link:hover { color: var(--navy-light); }
    .nav-link.active { border-bottom: 2px solid var(--navy); }
    .nav-label { cursor: default; user-select: none; }
    .nav-dropdown { position: relative; }
    .nav-dropdown:hover .dropdown-menu, .nav-dropdown:focus-within .dropdown-menu { opacity: 1; pointer-events: all; transform: translateX(-50%) translateY(0); }
    .dropdown-menu { position: absolute; top: 100%; left: 50%; transform: translateX(-50%) translateY(-6px); background: var(--white); border: 1px solid rgba(26,45,74,0.15); min-width: 200px; padding: 8px 0; opacity: 0; pointer-events: none; transition: opacity 0.2s, transform 0.2s; z-index: 100; }
    .dropdown-menu a { display: block; font-size: 12px; font-weight: 500; letter-spacing: 0.07em; text-transform: uppercase; color: var(--navy); text-decoration: none; padding: 10px 18px; transition: background 0.15s; }
    .dropdown-menu a:hover { background: #eceff1; }

    /* ─── HAMBURGER ───────────────────────────────────────────── */
    .hamburger-btn { display: none; flex-direction: column; gap: 5px; align-items: flex-start; background: none; border: none; cursor: pointer; padding: 4px; }
    .hamburger-btn span { display: block; height: 2px; background: var(--navy); transition: all 0.25s ease; }
    .hamburger-btn span:nth-child(1) { width: 24px; }
    .hamburger-btn span:nth-child(2) { width: 17px; }
    .hamburger-btn span:nth-child(3) { width: 24px; }
    .hamburger-btn.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); width: 24px; }
    .hamburger-btn.open span:nth-child(2) { opacity: 0; }
    .hamburger-btn.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); width: 24px; }

    /* ─── MOBILE NAV ──────────────────────────────────────────── */
    .mobile-nav { display: none; position: fixed; inset: 0; background: var(--white); z-index: 200; flex-direction: column; align-items: center; justify-content: center; gap: 4px; opacity: 0; pointer-events: none; transition: opacity 0.25s ease; }
    .mobile-nav.open { opacity: 1; pointer-events: all; }
    .mobile-nav-close { position: absolute; top: 24px; right: 24px; background: none; border: none; font-size: 24px; color: var(--navy); cursor: pointer; padding: 8px; }
    .mobile-nav a { font-family: 'Barlow Condensed', sans-serif; font-size: 30px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: var(--navy); text-decoration: none; padding: 8px 24px; }
    .mobile-nav-group { width: 100%; display: flex; flex-direction: column; align-items: center; }
    .mobile-nav-toggle { font-family: 'Barlow Condensed', sans-serif; font-size: 30px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: var(--navy); background: none; border: none; cursor: pointer; padding: 8px 24px; display: flex; align-items: center; gap: 8px; }
    .mobile-nav-toggle .caret { font-size: 18px; transition: transform 0.2s; display: inline-block; }
    .mobile-nav-toggle[aria-expanded="true"] .caret { transform: rotate(180deg); }
    .mobile-nav-sub { display: flex; flex-direction: column; align-items: center; gap: 0; width: 100%; padding-bottom: 4px; max-height: 0; overflow: hidden; opacity: 0; transition: max-height 0.35s ease, opacity 0.25s ease 0.2s; }
    .mobile-nav-sub.open { max-height: 320px; opacity: 1; }
    .mobile-nav-sub a { font-family: 'Barlow', sans-serif !important; font-size: 14px !important; font-weight: 500 !important; letter-spacing: 0.08em !important; color: var(--text-muted) !important; padding: 6px 24px !important; text-transform: uppercase; }

    /* ─── RESPONSIVE HEADER ───────────────────────────────────── */
    @media (max-width: 960px) {
      .logo-row { display: grid; grid-template-columns: 44px 1fr 44px; align-items: center; padding: 20px; }
      .hamburger-btn { display: flex; grid-column: 1; }
      .logo-placeholder { grid-column: 2; justify-self: center; font-size: 20px; }
      .nav-row { display: none; }
    }

    /* ─── FOOTER ─────────────────────────────────────────────── */
    .site-footer { background: var(--navy); padding: 64px 40px 32px; }
    .footer-inner { max-width: 1100px; margin: 0 auto; }
    .footer-top { display: grid; grid-template-columns: 1fr auto 1fr; gap: 40px; align-items: start; padding-bottom: 48px; border-bottom: 1px solid rgba(255,255,255,0.1); }
    .footer-brand { display: flex; flex-direction: column; gap: 16px; }
    .footer-logo { font-family: 'Barlow Condensed', sans-serif; font-size: 22px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--white); text-decoration: none; }
    .footer-tagline { font-size: 13px; font-weight: 400; line-height: 1.7; color: var(--blue-grey); max-width: 260px; }
    .footer-contact { display: flex; flex-direction: column; gap: 10px; text-align: center; align-items: center; }
    .footer-contact-label { font-size: 10px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--blue-grey); margin-bottom: 4px; }
    .footer-address { font-size: 13.5px; font-weight: 400; line-height: 1.7; color: rgba(255,255,255,0.75); text-align: center; }
    .footer-phone { font-family: 'Barlow Condensed', sans-serif; font-size: 22px; font-weight: 600; letter-spacing: 0.06em; color: var(--white); text-decoration: none; transition: color 0.2s; }
    .footer-phone:hover { color: var(--blue-grey); }
    .footer-social { display: flex; flex-direction: column; align-items: flex-end; gap: 16px; }
    .footer-social-label { font-size: 10px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--blue-grey); }
    .footer-social-icons { display: flex; flex-wrap: wrap; gap: 10px; justify-content: flex-end; }
    .footer-social-link { width: 38px; height: 38px; border: 1px solid rgba(255,255,255,0.15); display: flex; align-items: center; justify-content: center; transition: border-color 0.2s, background 0.2s; flex-shrink: 0; }
    .footer-social-link:hover { border-color: rgba(255,255,255,0.5); background: rgba(255,255,255,0.07); }
    .footer-social-link svg { width: 16px; height: 16px; fill: rgba(255,255,255,0.75); display: block; transition: fill 0.2s; }
    .footer-social-link:hover svg { fill: var(--white); }
    .footer-bottom { display: flex; align-items: center; justify-content: space-between; padding-top: 28px; gap: 16px; flex-wrap: wrap; }
    .footer-legal { font-size: 11.5px; color: rgba(255,255,255,0.35); line-height: 1.6; }
    .footer-links { display: flex; gap: 20px; flex-wrap: wrap; }
    .footer-links a { font-size: 11px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: rgba(255,255,255,0.35); text-decoration: none; transition: color 0.2s; }
    .footer-links a:hover { color: rgba(255,255,255,0.7); }

    @media (max-width: 900px) {
      .site-footer { padding: 52px 24px 28px; }
      .footer-top { grid-template-columns: 1fr; gap: 40px; }
      .footer-social { align-items: flex-start; }
      .footer-social-icons { justify-content: flex-start; }
      .footer-contact { align-items: flex-start; text-align: left; }
      .footer-address { text-align: left; }
      .footer-bottom { flex-direction: column; align-items: flex-start; gap: 12px; }
    }

    /* ─── YOUR PAGE STYLES GO HERE ───────────────────────────── */

  </style>
</head>
<body>

<!-- ═══ HEADER ════════════════════════════════════════════════ -->
<header class="site-header" role="banner">
  <div class="logo-row">
    <button class="hamburger-btn" id="hamburgerBtn" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
    <a href="/" class="logo-placeholder">Morandi Properties</a>
  </div>
  <nav class="nav-row" role="navigation" aria-label="Primary navigation">
    <a href="/" class="nav-link">Home</a>
    <div class="nav-dropdown">
      <span class="nav-link nav-label">Buying ▾</span>
      <div class="dropdown-menu">
        <a href="https://morandiproperties.com/buying/listings">Current Listings</a>
        <a href="https://morandiproperties.com/buying/open-house">Open House Search</a>
        <a href="https://morandiproperties.com/buying/buying-strategy-guide">Buyer's Strategy Guide</a>
        <a href="https://morandiproperties.com/buying/calculator">Mortgage Calculator</a>
      </div>
    </div>
    <div class="nav-dropdown">
      <span class="nav-link nav-label">Selling ▾</span>
      <div class="dropdown-menu">
        <a href="https://morandiproperties.com/selling/sold-portfolio">Sold Portfolio</a>
        <a href="https://morandiproperties.com/selling/selling-strategy-guide">Seller's Strategy Guide</a>
        <a href="https://morandiproperties.com/selling/valuation">What is my Home Worth?</a>
      </div>
    </div>
    <div class="nav-dropdown">
      <span class="nav-link nav-label">Insights ▾</span>
      <div class="dropdown-menu">
        <a href="https://morandiproperties.com/insights/neighborhood-spotlights">Neighborhood Spotlights</a>
        <a href="https://morandiproperties.com/insights/faq">Real Estate Q&amp;A</a>
      </div>
    </div>
    <div class="nav-dropdown">
      <span class="nav-link nav-label">Realtors ▾</span>
      <div class="dropdown-menu">
        <a href="https://morandiproperties.com/realtors/agents">Meet the Team</a>
        <a href="https://morandiproperties.com/realtors/ray-morandi">Meet Ray Morandi</a>
        <a href="https://morandiproperties.com/realtors/reviews">Client Reviews</a>
      </div>
    </div>
    <div class="nav-dropdown">
      <span class="nav-link nav-label">Contact ▾</span>
      <div class="dropdown-menu">
        <a href="https://morandiproperties.com/contact/office">General Inquiry</a>
        <a href="https://morandiproperties.com/contact/chicagoland-market-report">Market Insider</a>
        <a href="https://morandiproperties.com/contact/social">Social Media Hub</a>
      </div>
    </div>
  </nav>
</header>

<!-- ═══ MAIN CONTENT — BUILD HERE ════════════════════════════ -->
<main role="main">

  <!-- YOUR PAGE CONTENT GOES HERE -->

</main>
<!-- ════════════════════════════════════════════════════════════ -->

<!-- ─── FOOTER ────────────────────────────────────────────────── -->
<footer class="site-footer" role="contentinfo" itemscope itemtype="https://schema.org/WPFooter">
  <div class="footer-inner">
    <div class="footer-top">
      <div class="footer-brand">
        <a href="/" class="footer-logo">Morandi Properties</a>
        <p class="footer-tagline">Helping Chicagoland families buy and sell homes in Orland Park, Tinley Park, Frankfort, Mokena, and New Lenox since 2006.</p>
      </div>
      <div class="footer-contact" itemscope itemtype="https://schema.org/RealEstateAgent">
        <span class="footer-contact-label">Get In Touch</span>
        <p class="footer-address" itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">
          <span itemprop="streetAddress">123 Main Street, Suite 100</span><br>
          <span itemprop="addressLocality">Orland Park</span>, <span itemprop="addressRegion">IL</span> <span itemprop="postalCode">60462</span>
        </p>
        <a href="tel:+17085550000" class="footer-phone" itemprop="telephone">(708) 555-0000</a>
      </div>
      <div class="footer-social">
        <span class="footer-social-label">Follow Along</span>
        <div class="footer-social-icons">
          <a href="#" class="footer-social-link" aria-label="Facebook" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24"><path d="M24 12.073C24 5.404 18.627 0 12 0S0 5.404 0 12.073C0 18.1 4.388 23.094 10.125 24v-8.437H7.078v-3.49h3.047V9.41c0-3.025 1.792-4.697 4.533-4.697 1.312 0 2.686.236 2.686.236v2.97h-1.513c-1.491 0-1.956.93-1.956 1.886v2.267h3.328l-.532 3.49h-2.796V24C19.612 23.094 24 18.1 24 12.073z"/></svg>
          </a>
          <a href="#" class="footer-social-link" aria-label="Instagram" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
          </a>
          <a href="#" class="footer-social-link" aria-label="LinkedIn" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
          </a>
          <a href="#" class="footer-social-link" aria-label="TikTok" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>
          </a>
          <a href="#" class="footer-social-link" aria-label="YouTube" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24"><path d="M23.495 6.205a3.007 3.007 0 00-2.088-2.088c-1.87-.501-9.396-.501-9.396-.501s-7.507-.01-9.396.501A3.007 3.007 0 00.527 6.205a31.247 31.247 0 00-.522 5.805 31.247 31.247 0 00.522 5.783 3.007 3.007 0 002.088 2.088c1.868.502 9.396.502 9.396.502s7.506 0 9.396-.502a3.007 3.007 0 002.088-2.088 31.247 31.247 0 00.5-5.783 31.247 31.247 0 00-.5-5.805zM9.609 15.601V8.408l6.264 3.602z"/></svg>
          </a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="footer-legal">
        &copy; 2026 Morandi Properties. All rights reserved.<br>
        Ray Morandi — Licensed Illinois Real Estate Broker &middot; License #PLACEHOLDER
      </p>
      <nav class="footer-links">
        <a href="/privacy">Privacy Policy</a>
        <a href="/terms">Terms of Use</a>
        <a href="https://morandiproperties.com/contact/office">Contact</a>
        <a href="https://morandiproperties.com/buying/listings">Current Listings</a>
      </nav>
    </div>
  </div>
</footer>

<!-- ═══ MOBILE NAV OVERLAY ════════════════════════════════════ -->
<nav class="mobile-nav" id="mobileNav" aria-label="Mobile navigation">
  <button class="mobile-nav-close" id="mobileNavClose" aria-label="Close menu">✕</button>
  <a href="/">Home</a>
  <div class="mobile-nav-group">
    <button class="mobile-nav-toggle" aria-expanded="false" data-target="mnBuying">Buying <span class="caret">▾</span></button>
    <div class="mobile-nav-sub" id="mnBuying">
      <a href="https://morandiproperties.com/buying/listings">Current Listings</a>
      <a href="https://morandiproperties.com/buying/open-house">Open House Search</a>
      <a href="https://morandiproperties.com/buying/buying-strategy-guide">Buyer's Strategy Guide</a>
      <a href="https://morandiproperties.com/buying/calculator">Mortgage Calculator</a>
    </div>
  </div>
  <div class="mobile-nav-group">
    <button class="mobile-nav-toggle" aria-expanded="false" data-target="mnSelling">Selling <span class="caret">▾</span></button>
    <div class="mobile-nav-sub" id="mnSelling">
      <a href="https://morandiproperties.com/selling/sold-portfolio">Sold Portfolio</a>
      <a href="https://morandiproperties.com/selling/selling-strategy-guide">Seller's Strategy Guide</a>
      <a href="https://morandiproperties.com/selling/valuation">What is my Home Worth?</a>
    </div>
  </div>
  <div class="mobile-nav-group">
    <button class="mobile-nav-toggle" aria-expanded="false" data-target="mnInsights">Insights <span class="caret">▾</span></button>
    <div class="mobile-nav-sub" id="mnInsights">
      <a href="https://morandiproperties.com/insights/neighborhood-spotlights">Neighborhood Spotlights</a>
      <a href="https://morandiproperties.com/insights/faq">Real Estate Q&amp;A</a>
    </div>
  </div>
  <div class="mobile-nav-group">
    <button class="mobile-nav-toggle" aria-expanded="false" data-target="mnTeam">Realtors <span class="caret">▾</span></button>
    <div class="mobile-nav-sub" id="mnTeam">
      <a href="https://morandiproperties.com/realtors/agents">Meet the Team</a>
      <a href="https://morandiproperties.com/realtors/ray-morandi">Meet Ray Morandi</a>
      <a href="https://morandiproperties.com/realtors/reviews">Client Reviews</a>
    </div>
  </div>
  <div class="mobile-nav-group">
    <button class="mobile-nav-toggle" aria-expanded="false" data-target="mnContact">Contact <span class="caret">▾</span></button>
    <div class="mobile-nav-sub" id="mnContact">
      <a href="https://morandiproperties.com/contact/office">General Inquiry</a>
      <a href="https://morandiproperties.com/contact/chicagoland-market-report">Market Insider</a>
      <a href="https://morandiproperties.com/contact/social">Social Media Hub</a>
    </div>
  </div>
</nav>

<script>
  // ── Mobile nav open/close ────────────────────────────────────
  const hBtn = document.getElementById('hamburgerBtn');
  const mNav = document.getElementById('mobileNav');
  const mCls = document.getElementById('mobileNavClose');
  function openNav()  { mNav.style.display='flex'; requestAnimationFrame(()=>mNav.classList.add('open')); hBtn.classList.add('open'); document.body.style.overflow='hidden'; }
  function closeNav() { mNav.classList.remove('open'); hBtn.classList.remove('open'); document.body.style.overflow=''; setTimeout(()=>mNav.style.display='none',250); }
  hBtn.addEventListener('click', openNav);
  mCls.addEventListener('click', closeNav);
  mNav.addEventListener('click', e=>{ if(e.target.tagName==='A') closeNav(); });
  document.addEventListener('keydown', e=>{ if(e.key==='Escape') closeNav(); });

  // ── Mobile nav accordion ─────────────────────────────────────
  document.querySelectorAll('.mobile-nav-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const sub = document.getElementById(btn.dataset.target);
      const isOpen = sub.classList.contains('open');
      document.querySelectorAll('.mobile-nav-sub').forEach(s => s.classList.remove('open'));
      document.querySelectorAll('.mobile-nav-toggle').forEach(b => b.setAttribute('aria-expanded','false'));
      if (!isOpen) { sub.classList.add('open'); btn.setAttribute('aria-expanded','true'); }
    });
  });
</script>

</body>
</html>
Legal & Copyright

Copyright © 2026 Morandi Properties LLC. > Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Disclaimer: All property data, valuations, and market insights provided on this site are for informational purposes only. Morandi Properties LLC makes no guarantees regarding the accuracy of this data. Use of this site does not constitute a broker-client relationship.
