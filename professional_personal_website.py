# Professional Portfolio Website — Neon Aura, Section Cards, Lightbox, Email Feedback

from flask import Flask, render_template_string, send_from_directory, abort, url_for, request, jsonify
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# ---------- CONFIG (EDIT THIS) ----------
# Where feedback emails should go
OWNER_EMAIL = os.environ.get("PORTFOLIO_OWNER_EMAIL", "tharunr2121@gmail.com")

# SMTP settings (set these as environment variables on Vercel / local .env)
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "tharunr2121@gmail.com")
SMTP_PASS = os.environ.get("SMTP_PASS", "tharun!it")

# ---------- PERSON DATA ----------
PERSON = {
    "name": "THARUN R",
    "title": "Software Engineer • CYBER SECURITY Enthusiast • Model & Dancer",
    "linkedin": "https://www.linkedin.com/in/tharun021/",
    "github": "https://github.com/tharunprinz", 
    "email": "tharunr2121@gmail.com",
    "youtube": "https://www.youtube.com/@tharunr21",
    "instagram": "https://www.instagram.com/thxrun21/",
    "profile_image": "profile.jpeg",
    "resume_filename": "resume.pdf",
    "model_9_16": [
        "model1.jpeg", "model2.jpeg", "model3.jpeg",
        "model4.jpg", "model5.jpeg", "model6.jpeg"
    ],
    "model_16_9": ["wide1.jpg", "wide2.jpg"],
    "dance_video_id": "vC0yDgson3Y",
    "dance_video_title": "Dhruva 2k21 at KCE",
    "dance_video_url": "https://youtu.be/vC0yDgson3Y",
    "projects": [
        {"title": "Ecommerce Site", "desc": "Responsive ecommerce UI using HTML, CSS, JS"},
        {"title": "Face Recognition", "desc": "Detects registered persons using Python and OpenCV"},
        {"title": "Malware Scanner Using Yara", "desc": "Detects malware-infected files via YARA rules"}
    ],
    "certifications": [
        {"title": "CYBER SECURITY AND NETWORKING 2k24", "issuer": "SYSTECH"},
        {"title": "Diploma in Computer Programming (C, C++, Python) 2023", "issuer": "IFC-INFOTECH Computer Education"}
    ],
    "achievements": [
        "Winner — Application Development (National Science Day) at KCE College (1st Prize, 2k23)",
        "RUNWAY MODEL — Aura Fashion Castle 2k25",
        "Salesforce Trailhead Agentblazer Champion and Innovator badge"
    ],
    "participations": [
        "National-level Generative AI Hackathon at Manakula Vinayaka College 2k23 (Pondicherry)",
        "Googlethon - Generative AI Hackathon at SNS College 2k23",
        "Materials Data Science Workshop at IIT Madras 2024",
        "Dance performances at multiple college fests"
    ]
}

# In-memory public feedback list (not persisted across restarts)
PUBLIC_FEEDBACK = []

# ------------- HTML TEMPLATE -------------
INDEX_HTML = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{{ person.name }} — {{ person.title }}</title>

  <link href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/typed.js@2.0.12"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

  <style>
    :root{
      --bg-1:#071124;
      --bg-2:#0b1830;
      --accent:#6ee7b7;
      --accent-soft:rgba(110,231,183,0.25);
      --muted:#9aa4b2;
      --glass:rgba(255,255,255,0.04);
      --border-soft:rgba(148,163,184,0.25);
      --card-shadow:0 18px 45px rgba(15,23,42,0.85);
      font-family:Inter,system-ui,"Segoe UI",Roboto,Arial;
    }
    html,body{
      margin:0;
      background:radial-gradient(circle at top,#0f172a 0,#020617 52%,#000 100%);
      color:#e2ebff;
      overflow-x:hidden;
    }
    .container{
      max-width:1100px;
      margin:28px auto 40px;
      padding:16px;
    }

    /* HERO + AURA */
    .hero{
      text-align:center;
      margin-bottom:28px;
      position:relative;
    }
    .aura-wrapper{
      position:relative;
      width:190px;
      height:190px;
      margin:0 auto 8px;
    }
    .aura{
      position:absolute;
      inset:0;
      border-radius:50%;
      background:
        radial-gradient(circle at 30% 20%, rgba(110,231,183,0.7), transparent 60%),
        radial-gradient(circle at 70% 80%, rgba(59,130,246,0.6), transparent 60%);
      filter:blur(20px);
      animation:pulse 3s infinite ease-in-out;
      opacity:.75;
    }
    .aura-ring{
      position:absolute;
      inset:-6px;
      border-radius:50%;
      border:1px dashed rgba(148,163,184,0.55);
      animation:spin 14s linear infinite;
      pointer-events:none;
    }
    .hero-pfp{
      position:relative;
      width:190px;
      height:190px;
      border-radius:50%;
      object-fit:cover;
      border:3px solid rgba(248,250,252,0.14);
      box-shadow:0 22px 40px rgba(15,23,42,0.9);
      z-index:2;
    }
    @keyframes pulse{
      0%{transform:scale(1);opacity:.6}
      50%{transform:scale(1.25);opacity:1}
      100%{transform:scale(1);opacity:.6}
    }
    @keyframes spin{
      from{transform:rotate(0deg);}
      to{transform:rotate(360deg);}
    }
    h1{
      margin:10px 0 0;
      font-size:32px;
      letter-spacing:0.04em;
    }
    .subtitle{
      color:var(--muted);
      margin-top:6px;
      font-size:17px;
      min-height:24px;
    }
    .lead{
      color:#cfeef0;
      line-height:1.5;
      margin:10px auto 0;
      max-width:620px;
      font-size:15px;
    }

    /* BUTTONS */
    .buttons{
      display:flex;
      gap:10px;
      flex-wrap:wrap;
      justify-content:center;
      margin-top:16px;
    }
    .btn{
      padding:8px 13px;
      border-radius:999px;
      border:1px solid rgba(148,163,184,0.45);
      background:linear-gradient(135deg,rgba(15,23,42,0.9),rgba(15,23,42,0.6));
      display:flex;
      gap:8px;
      align-items:center;
      color:#eaf4ff;
      text-decoration:none;
      font-size:14px;
      box-shadow:0 10px 24px rgba(15,23,42,0.8);
      backdrop-filter:blur(10px);
      transition:transform .2s ease, box-shadow .2s ease, border-color .2s ease, background .2s ease;
    }
    .btn i{font-size:15px;}
    .btn:hover{
      transform:translateY(-4px);
      box-shadow:0 18px 35px rgba(15,23,42,0.95);
      border-color:var(--accent-soft);
      background:linear-gradient(135deg,rgba(15,23,42,0.95),rgba(30,64,175,0.85));
    }
    .btn.primary{
      background:linear-gradient(135deg,rgba(56,189,248,0.16),rgba(129,230,217,0.2));
      border-color:rgba(94,234,212,0.5);
    }
    .btn.small{
      padding:6px 11px;
      font-size:13px;
      box-shadow:none;
    }

    /* SECTION CARDS */
    .section-card{
      margin-top:22px;
      padding:18px 20px 18px;
      border-radius:18px;
      background:
        radial-gradient(circle at top left, rgba(56,189,248,0.08), transparent 60%),
        radial-gradient(circle at bottom right, rgba(129,230,217,0.06), transparent 55%),
        rgba(15,23,42,0.9);
      border:1px solid var(--border-soft);
      box-shadow:var(--card-shadow);
      backdrop-filter:blur(12px);
    }
    .section-header{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      margin-bottom:10px;
    }
    .section-title{
      font-size:18px;
      letter-spacing:.04em;
      text-transform:uppercase;
      color:#e5edff;
    }
    .section-tag{
      font-size:11px;
      text-transform:uppercase;
      letter-spacing:.16em;
      color:var(--muted);
      padding:4px 10px;
      border-radius:999px;
      border:1px solid rgba(148,163,184,0.3);
      background:rgba(15,23,42,0.8);
    }

    /* LIST STYLES */
    .pill-list{
      display:flex;
      flex-direction:column;
      gap:10px;
      margin:0;
      padding:0;
      list-style:none;
    }
    .pill-item{
      padding:10px 12px;
      border-radius:12px;
      border:1px solid rgba(148,163,184,0.35);
      background:linear-gradient(135deg,rgba(15,23,42,0.85),rgba(15,23,42,0.65));
    }
    .pill-item-title{
      font-weight:600;
      font-size:14px;
    }
    .pill-item-sub{
      color:var(--muted);
      font-size:13px;
      margin-top:2px;
    }
    .bullet-list{
      margin:0;
      padding-left:18px;
      color:#d1e5ff;
      font-size:14px;
    }
    .bullet-list li{
      margin-bottom:5px;
    }

    /* DANCE VIDEO */
    .dance-card{
      display:flex;
      gap:16px;
      align-items:stretch;
      flex-wrap:wrap;
    }
    .dance-thumb{
      display:block;
      max-width:360px;
      border-radius:16px;
      overflow:hidden;
      position:relative;
      flex:0 0 auto;
      box-shadow:0 18px 40px rgba(0,0,0,0.85);
      border:1px solid rgba(30,64,175,0.7);
    }
    .dance-thumb img{
      width:100%;
      display:block;
      transition:transform .25s ease;
    }
    .dance-thumb::after{
      content:"Watch on YouTube";
      position:absolute;
      bottom:8px;
      right:10px;
      padding:4px 10px;
      border-radius:999px;
      background:rgba(15,23,42,0.86);
      border:1px solid rgba(148,163,184,0.7);
      font-size:11px;
      color:#e5edff;
    }
    .dance-thumb:hover img{
      transform:scale(1.03);
    }
    .dance-meta{
      flex:1 1 220px;
      display:flex;
      flex-direction:column;
      justify-content:center;
      gap:6px;
      min-width:0;
    }
    .dance-meta-title{
      font-size:17px;
      font-weight:600;
    }
    .dance-meta-sub{
      font-size:13px;
      color:var(--muted);
    }

    /* MODELING */
    .portfolio-wrapper{
      display:flex;
      flex-direction:column;
      gap:16px;
    }
    .vertical-gallery{
      display:grid;
      grid-template-columns:repeat(3, minmax(0, 1fr));
      gap:12px;
      justify-content:center;
    }
    .vertical-tile, .wide-tile{
      border-radius:14px;
      overflow:hidden;
      background:#020617;
      box-shadow:0 14px 35px rgba(0,0,0,0.9);
      cursor:pointer;
      position:relative;
      border:1px solid rgba(15,23,42,0.9);
    }
    .vertical-tile::before{content:"";display:block;padding-top:177%;}
    .vertical-tile img{
      position:absolute;
      inset:0;
      width:100%;
      height:100%;
      object-fit:cover;
      transition:transform .25s ease, filter .25s ease;
    }
    .vertical-tile:hover img{
      transform:scale(1.05);
      filter:brightness(1.08);
    }
    .wide-gallery{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:12px;
    }
    .wide-tile::before{content:"";display:block;padding-top:56.25%;}
    .wide-tile img{
      position:absolute;
      inset:0;
      width:100%;
      height:100%;
      object-fit:cover;
      transition:transform .25s ease, filter .25s ease;
    }
    .wide-tile:hover img{
      transform:scale(1.04);
      filter:brightness(1.06);
    }

    /* FEEDBACK */
    .feedback-box textarea{
      width:100%;
      height:90px;
      border-radius:12px;
      border:1px solid rgba(148,163,184,0.45);
      padding:10px 12px;
      background:rgba(15,23,42,0.95);
      color:#eaf4ff;
      font-size:14px;
      resize:none;
      outline:none;
    }
    .feedback-box textarea::placeholder{
      color:rgba(148,163,184,0.8);
    }
    .feedback-row{
      display:flex;
      flex-wrap:wrap;
      gap:10px;
      margin:10px 0;
      font-size:13px;
      color:var(--muted);
    }
    .feedback-row input{
      border-radius:999px;
      border:1px solid rgba(148,163,184,0.45);
      padding:6px 10px;
      background:rgba(15,23,42,0.95);
      color:#eaf4ff;
      outline:none;
    }
    .visibility-choice{
      display:flex;
      gap:8px;
      align-items:center;
      font-size:13px;
    }
    .visibility-choice label{display:flex;gap:4px;align-items:center;}

    .feedback-box button{
      margin-top:6px;
      padding:9px 16px;
      border-radius:999px;
      background:linear-gradient(135deg,rgba(129,230,217,0.25),rgba(56,189,248,0.3));
      border:1px solid rgba(94,234,212,0.8);
      color:#f9fafb;
      cursor:pointer;
      font-size:14px;
      font-weight:500;
      display:inline-flex;
      align-items:center;
      gap:6px;
      box-shadow:0 12px 30px rgba(15,23,42,0.9);
      transition:transform .2s ease, box-shadow .2s ease;
    }
    .feedback-box button:hover{
      transform:translateY(-3px);
      box-shadow:0 18px 40px rgba(15,23,42,1);
    }
    .feedback-status{
      margin-top:8px;
      font-size:13px;
      color:var(--muted);
    }
    .public-feedback-list{
      margin:12px 0 0;
      padding-left:16px;
      font-size:13px;
      color:#d1e5ff;
    }

    /* LIGHTBOX */
    .lightbox{
      position:fixed;
      inset:0;
      background:rgba(3,6,12,0.9);
      display:none;
      align-items:center;
      justify-content:center;
      z-index:9999;
      padding:24px;
    }
    .lightbox.open{display:flex;}
    .lightbox-content{
      max-width:1100px;
      width:100%;
      max-height:90vh;
      display:grid;
      grid-template-columns:1fr 320px;
      gap:18px;
    }
    .lightbox-img{
      background:#020617;
      border-radius:16px;
      padding:10px;
      display:flex;
      align-items:center;
      justify-content:center;
      border:1px solid rgba(30,64,175,0.7);
      box-shadow:0 24px 60px rgba(0,0,0,0.95);
    }
    .lightbox-img img{
      max-width:100%;
      max-height:86vh;
      object-fit:contain;
      display:block;
    }
    .lightbox-side{
      color:#eaf4ff;
      display:flex;
      flex-direction:column;
      justify-content:space-between;
      gap:12px;
    }
    .side-actions{
      display:flex;
      gap:10px;
      flex-wrap:wrap;
      margin-top:6px;
    }
    .action-btn{
      padding:9px 12px;
      border-radius:999px;
      background:rgba(15,23,42,0.95);
      border:1px solid rgba(148,163,184,0.6);
      cursor:pointer;
      display:inline-flex;
      align-items:center;
      gap:8px;
      font-size:13px;
    }
    .action-btn i{font-size:14px;}
    .lightbox-note{
      margin-top:10px;
      color:var(--muted);
      font-size:12px;
    }

    @media(max-width:900px){
      .lightbox-content{grid-template-columns:1fr;}
      .lightbox-side{order:-1;}
    }
    @media(max-width:720px){
      .vertical-gallery{grid-template-columns:repeat(2,minmax(0,1fr));}
      .wide-gallery{grid-template-columns:1fr;}
    }
  </style>
</head>
<body>
  <div class="container">

    <!-- HERO -->
    <div class="hero" data-aos="fade-up">
      <div class="aura-wrapper">
        <div class="aura"></div>
        <div class="aura-ring"></div>
        <img src="{{ url_for('static', filename=person.profile_image) }}" class="hero-pfp" alt="Profile">
      </div>

      <h1>{{ person.name }}</h1>
      <div class="subtitle"><span id="typed"></span></div>
      <p class="lead">
        I build secure systems, perform on stage, and model — blending technology with creativity.
      </p>

      <div class="buttons">
        <a class="btn primary" href="{{ person.linkedin }}" target="_blank">
          <i class="fa-brands fa-linkedin"></i> LinkedIn
        </a>
        <a class="btn" href="{{ url_for('download_resume') }}">
          <i class="fa-solid fa-file-arrow-down"></i> Resume
        </a>
        <a class="btn" href="{{ person.github }}" target="_blank">
          <i class="fa-brands fa-github"></i> GitHub
        </a>
        <a class="btn" href="mailto:{{ person.email }}">
          <i class="fa-solid fa-envelope"></i> Email
        </a>
        <a class="btn" href="{{ person.youtube }}" target="_blank">
          <i class="fa-brands fa-youtube"></i> YouTube
        </a>
        <a class="btn" href="{{ person.instagram }}" target="_blank">
          <i class="fa-brands fa-instagram"></i> Instagram
        </a>
      </div>
    </div>

    <!-- PROJECTS -->
    <section class="section-card" data-aos="fade-up">
      <div class="section-header">
        <h3 class="section-title">Projects</h3>
        <span class="section-tag">Tech • Builds</span>
      </div>
      <ul class="pill-list">
        {% for p in person.projects %}
        <li class="pill-item">
          <div class="pill-item-title">{{ p.title }}</div>
          <div class="pill-item-sub">{{ p.desc }}</div>
        </li>
        {% endfor %}
      </ul>
    </section>

    <!-- CERTIFICATIONS -->
    <section class="section-card" data-aos="fade-up">
      <div class="section-header">
        <h3 class="section-title">Certifications</h3>
        <span class="section-tag">Verified Skills</span>
      </div>
      <ul class="pill-list">
        {% for c in person.certifications %}
        <li class="pill-item">
          <div class="pill-item-title">{{ c.title }}</div>
          <div class="pill-item-sub">{{ c.issuer }}</div>
        </li>
        {% endfor %}
      </ul>
    </section>

    <!-- ACHIEVEMENTS -->
    <section class="section-card" data-aos="fade-up">
      <div class="section-header">
        <h3 class="section-title">Achievements</h3>
        <span class="section-tag">Highlights</span>
      </div>
      <ul class="bullet-list">
        {% for a in person.achievements %}
        <li>{{ a }}</li>
        {% endfor %}
      </ul>
    </section>

    <!-- PARTICIPATIONS -->
    <section class="section-card" data-aos="fade-up">
      <div class="section-header">
        <h3 class="section-title">Participations</h3>
        <span class="section-tag">Involvement</span>
      </div>
      <ul class="bullet-list">
        {% for p in person.participations %}
        <li>{{ p }}</li>
        {% endfor %}
      </ul>
    </section>

    <!-- FEATURED DANCE VIDEO (title stays "Featured Dance Video") -->
    <section class="section-card" data-aos="fade-up">
      <div class="section-header">
        <h3 class="section-title">Featured Dance Video</h3>
        <span class="section-tag">Stage • Performance</span>
      </div>

      <div class="dance-card">
        <a href="{{ person.dance_video_url }}" class="dance-thumb" target="_blank" rel="noopener">
          <img src="https://img.youtube.com/vi/{{ person.dance_video_id }}/hqdefault.jpg"
               alt="Featured dance video thumbnail">
        </a>
        <div class="dance-meta">
          <div class="dance-meta-title">{{ person.dance_video_title }}</div>
          <div class="dance-meta-sub">
            High-energy performance from the Dhruva cultural fest at Karpagam College of Engineering.
          </div>
          <div style="margin-top:8px;">
            <a href="{{ person.dance_video_url }}" class="btn small" target="_blank" rel="noopener">
              <i class="fa-brands fa-youtube"></i> Watch on YouTube
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- MODELING PORTFOLIO -->
    <section class="section-card" data-aos="fade-up">
      <div class="section-header">
        <h3 class="section-title">Modeling Portfolio</h3>
        <span class="section-tag">Visual • Frames</span>
      </div>

      <div class="portfolio-wrapper">
        <div class="vertical-gallery">
          {% for img in person.model_9_16 %}
          <div class="vertical-tile" data-fname="{{ img }}" data-full="{{ url_for('static', filename=img) }}">
            <img src="{{ url_for('static', filename=img) }}" alt="model {{ loop.index }}">
          </div>
          {% endfor %}
        </div>

        <div class="wide-gallery">
          {% for img in person.model_16_9 %}
          <div class="wide-tile" data-fname="{{ img }}" data-full="{{ url_for('static', filename=img) }}">
            <img src="{{ url_for('static', filename=img) }}" alt="wide image {{ loop.index }}">
          </div>
          {% endfor %}
        </div>
      </div>
    </section>

    <!-- FEEDBACK (BOTTOM TILE) -->
    <section class="section-card feedback-box" data-aos="fade-up">
      <div class="section-header">
        <h3 class="section-title">Share Your Feedback</h3>
        <span class="section-tag">Your Thoughts</span>
      </div>

      <textarea id="feedback-text"
        placeholder="How did you like this portfolio? Any suggestions, opportunities, or feedback are welcome."></textarea>

      <div class="feedback-row">
        <input id="fb-name" type="text" placeholder="Your name (optional)">
        <input id="fb-email" type="email" placeholder="Your email (optional)">
        <div class="visibility-choice">
          <span>Visibility:</span>
          <label><input type="radio" name="visibility" value="public" checked> Public</label>
          <label><input type="radio" name="visibility" value="private"> Private</label>
        </div>
      </div>

      <button id="feedback-submit">
        <i class="fa-solid fa-paper-plane"></i> Submit Feedback
      </button>
      <div id="feedback-status" class="feedback-status"></div>

      {% if public_feedback %}
      <div style="margin-top:12px;">
        <strong>Public Feedback:</strong>
        <ul class="public-feedback-list" id="public-feedback-list">
          {% for fb in public_feedback %}
          <li><strong>{{ fb.name }}</strong>: {{ fb.text }}</li>
          {% endfor %}
        </ul>
      </div>
      {% else %}
      <ul class="public-feedback-list" id="public-feedback-list" style="display:none;"></ul>
      {% endif %}
    </section>

  </div>

  <!-- LIGHTBOX -->
  <div id="lightbox" class="lightbox" role="dialog" aria-hidden="true">
    <div class="lightbox-content">
      <div class="lightbox-img">
        <img id="lightbox-image" src="" alt="Full image">
      </div>
      <div class="lightbox-side">
        <div>
          <h3 id="lb-fname">Image</h3>
          <div class="side-actions">
            <a id="lb-download" class="action-btn" href="#" download>
              <i class="fa-solid fa-arrow-down"></i> Download
            </a>
            <button id="lb-like" class="action-btn">
              <i class="fa-regular fa-heart"></i> <span id="lb-like-count">0</span>
            </button>
            <button id="lb-share" class="action-btn">
              <i class="fa-solid fa-share-nodes"></i> Share
            </button>
          </div>
        </div>
        <div class="lightbox-note">
          Click outside the box to close. Likes are stored locally on your device.
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
  <script>
    AOS.init({ duration:700, once:true });

    new Typed('#typed', {
      strings:[
        "{{ person.title }}",
        "Developer • Dancer • Model • Cybersecurity",
        "Open to work and collaborations"
      ],
      typeSpeed:36,
      backSpeed:25,
      loop:true
    });

    // LIGHTBOX JS
    const lightbox = document.getElementById('lightbox');
    const lbImage = document.getElementById('lightbox-image');
    const lbFname = document.getElementById('lb-fname');
    const lbDownload = document.getElementById('lb-download');
    const lbLike = document.getElementById('lb-like');
    const lbLikeCount = document.getElementById('lb-like-count');
    const lbShare = document.getElementById('lb-share');

    function openLightbox(src, filename){
      lbImage.src = src;
      lbFname.textContent = filename;
      lbDownload.href = src;
      lightbox.classList.add('open');
      lightbox.setAttribute('aria-hidden', 'false');

      const likes = JSON.parse(localStorage.getItem('img_likes') || '{}');
      const count = likes[filename] || 0;
      lbLikeCount.textContent = count;
      lbLike.dataset.file = filename;
      lbShare.dataset.file = filename;
      lbLike.innerHTML = '<i class="fa-regular fa-heart"></i> <span id="lb-like-count">'+count+'</span>';
    }

    function closeLightbox(){
      lightbox.classList.remove('open');
      lightbox.setAttribute('aria-hidden', 'true');
      lbImage.src = '';
    }

    document.querySelectorAll('.vertical-tile, .wide-tile').forEach(tile => {
      tile.addEventListener('click', () => {
        const src = tile.dataset.full || tile.querySelector('img').src;
        const fname = tile.dataset.fname || src.split('/').pop();
        openLightbox(src, fname);
      });
    });

    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });

    lbLike.addEventListener('click', () => {
      const file = lbLike.dataset.file;
      const likes = JSON.parse(localStorage.getItem('img_likes') || '{}');
      likes[file] = (likes[file] || 0) + 1;
      localStorage.setItem('img_likes', JSON.stringify(likes));
      const count = likes[file];
      lbLike.innerHTML =
        '<i class="fa-solid fa-heart" style="color:#ff6b81"></i> ' +
        '<span id="lb-like-count">'+count+'</span>';
    });

    lbShare.addEventListener('click', async () => {
      const file = lbShare.dataset.file;
      const url = location.origin + '/static/' + file;
      if (navigator.share) {
        try {
          await navigator.share({ title: 'Image - ' + file, url });
        } catch (err) {
          console.log('Share cancelled', err);
        }
      } else {
        try {
          await navigator.clipboard.writeText(url);
          alert('Image URL copied to clipboard');
        } catch (e) {
          prompt('Copy this URL', url);
        }
      }
    });

    // FEEDBACK JS (send to backend, email + public/private)
    const fbBtn = document.getElementById('feedback-submit');
    const fbText = document.getElementById('feedback-text');
    const fbName = document.getElementById('fb-name');
    const fbEmail = document.getElementById('fb-email');
    const fbStatus = document.getElementById('feedback-status');
    const fbPublicList = document.getElementById('public-feedback-list');

    fbBtn.addEventListener('click', async () => {
      const text = fbText.value.trim();
      const name = fbName.value.trim();
      const email = fbEmail.value.trim();
      const visibility = document.querySelector('input[name="visibility"]:checked').value;

      if (!text) {
        fbStatus.textContent = "Please enter some feedback before submitting.";
        return;
      }

      fbStatus.textContent = "Sending feedback...";
      try {
        const res = await fetch("{{ url_for('submit_feedback') }}", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({ text, name, email, visibility })
        });
        const data = await res.json();
        if (res.ok && data.ok) {
          fbStatus.textContent = data.message || "Thank you for your feedback!";
          fbText.value = "";
          // if public, update list
          if (data.feedback && data.feedback.length) {
            fbPublicList.style.display = "block";
            fbPublicList.innerHTML = "";
            data.feedback.forEach(item => {
              const li = document.createElement("li");
              li.innerHTML = "<strong>" + item.name + "</strong>: " + item.text;
              fbPublicList.appendChild(li);
            });
          }
        } else {
          fbStatus.textContent = data.message || "Server could not send feedback email.";
        }
      } catch (e) {
        fbStatus.textContent = "Network error while sending feedback.";
      }
    });
  </script>
</body>
</html>
"""

# ------------- EMAIL SENDER -------------
def send_feedback_email(text: str, visibility: str, name: str, email: str):
    """
    Sends feedback to OWNER_EMAIL using SMTP.
    If SMTP_* env vars are not set, just prints to console (local dev).
    """
    msg = EmailMessage()
    msg["Subject"] = f"Portfolio feedback ({visibility})"
    msg["From"] = OWNER_EMAIL
    msg["To"] = OWNER_EMAIL

    body_lines = []
    if name:
        body_lines.append(f"From: {name}")
    if email:
        body_lines.append(f"Reply-to email: {email}")
        msg["Reply-To"] = email
    body_lines.append(f"Visibility: {visibility}")
    body_lines.append("")
    body_lines.append("Feedback:")
    body_lines.append(text)

    msg.set_content("\n".join(body_lines))

    if not (SMTP_HOST and SMTP_USER and SMTP_PASS):
        # For local dev / if not configured, don't crash, just print.
        print("==== FEEDBACK EMAIL (SMTP not configured, not actually sent) ====")
        print(msg)
        return

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)


# ------------- ROUTES -------------
@app.route("/")
def index():
    return render_template_string(INDEX_HTML, person=PERSON, public_feedback=PUBLIC_FEEDBACK)


@app.route("/resume")
def download_resume():
    resume_path = os.path.join(app.static_folder or "static", PERSON["resume_filename"])
    if os.path.exists(resume_path):
        return send_from_directory(app.static_folder or "static", PERSON["resume_filename"], as_attachment=True)
    abort(404)


@app.route("/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    name = (data.get("name") or "").strip() or "Anonymous"
    email = (data.get("email") or "").strip()
    visibility = (data.get("visibility") or "private").lower()

    if not text:
        return jsonify(ok=False, message="Feedback text is required."), 400

    try:
        send_feedback_email(text=text, visibility=visibility, name=name, email=email)
    except Exception as e:
        # Log error and return message
        print("Error sending feedback email:", e)
        return jsonify(ok=False, message="Server could not send feedback email."), 500

    if visibility == "public":
        PUBLIC_FEEDBACK.append({"name": name, "text": text})

    return jsonify(
        ok=True,
        message="Thank you! Your feedback has been sent to my email.",
        feedback=PUBLIC_FEEDBACK
    )


if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)
