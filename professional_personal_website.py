# Full updated Flask app with lightbox

"""
Professional one-file Flask site — responsive, animated, model+dance portfolio,
projects + certifications, YouTube & Instagram links, resume download, and image lightbox.

Place your assets in ./static/ as listed below and run:
source .venv/bin/activate
python professional_personal_website.py
"""
from flask import Flask, render_template_string, send_from_directory, abort, url_for
import os

app = Flask(__name__)

PERSON = {
    "name": "THARUN R",
    "title": "Software Engineer • CYBER SECURITY Enthusiast • Model & Dancer",
    "linkedin": "https://www.linkedin.com/in/tharun021/",
    "email": "tharunr2121@gmail.com",
    "youtube": "https://www.youtube.com/@tharunr21",
    "instagram": "https://www.instagram.com/thxrun21/",
    "profile_image": "profile.jpeg",
    "resume_filename": "resume.pdf",
    "model_9_16": [
        "model1.jpeg","model2.jpeg","model3.jpeg",
        "model4.jpg","model5.jpeg","model6.jpeg"
    ],
    "model_16_9": ["wide1.jpg","wide2.jpg"],
    "dance_video_id": "vC0yDgson3Y",
    "dance_video_url": "https://youtu.be/vC0yDgson3Y",
    "projects": [
        {"title": "Secure API Platform","desc": "Design and implementation of auth-first microservices."},
        {"title": "ML Monitoring Pipeline","desc": "End-to-end pipeline for model validation & alerts."}
    ],
    "certifications": [
        {"title": "CEH (Certified Ethical Hacker)","issuer": "EC-Council"},
        {"title": "AWS Solutions Architect Associate","issuer": "Amazon"}
    ]
}

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
    :root{--bg-1:#071124;--bg-2:#0b1830;--accent:#6ee7b7;--muted:#9aa4b2;--glass:rgba(255,255,255,0.04);--card-shadow:0 12px 40px rgba(2,6,23,0.6);font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,Arial}
    html,body{margin:0;background:linear-gradient(var(--bg-1),var(--bg-2));color:#eaf4ff;overflow-x:hidden}
    .container{max-width:1100px;margin:28px auto;padding:16px;position:relative;z-index:2}
    .hero{display:grid;grid-template-columns:1fr 320px;gap:22px}
    .card{background:rgba(255,255,255,0.03);border-radius:14px;padding:18px;box-shadow:var(--card-shadow);backdrop-filter:blur(6px)}
    h1{margin:0;font-size:30px}.subtitle{color:var(--muted);margin-bottom:8px}.lead{color:#cfeef0;margin-top:8px;line-height:1.45}
    .buttons{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}.btn{padding:8px 12px;border-radius:10px;border:1px solid rgba(255,255,255,0.06);background:var(--glass);display:flex;gap:8px;align-items:center;text-decoration:none;color:#eaf4ff;transition:.2s}.btn:hover{transform:translateY(-6px);box-shadow:0 14px 30px rgba(0,0,0,0.5)}.btn.primary{background:linear-gradient(90deg,#6ee7b733,#7c3aed22)}
    .profile-panel{text-align:center;position:sticky;top:20px}.profile-panel img{width:150px;height:150px;border-radius:16px;object-fit:cover;border:3px solid rgba(255,255,255,0.04)}

    /* modeling gallery */
    .vertical-gallery{display:grid;grid-template-columns:repeat(3,160px);gap:12px;justify-content:center}
    .vertical-tile{width:160px;border-radius:10px;overflow:hidden;background:#061021;box-shadow:0 10px 30px rgba(0,0,0,0.45);position:relative;transition:.25s}
    .vertical-tile::before{content:"";display:block;padding-top:177.78%}
    .vertical-tile img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;cursor:pointer}
    .vertical-tile:hover{transform:translateY(-6px)}

    .wide-gallery{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}
.wide-tile{position:relative;border-radius:10px;overflow:hidden;background:#061021;box-shadow:0 12px 34px rgba(0,0,0,0.45)}
.wide-tile::before{content:"";display:block;padding-top:56.25%} /* 16:9 ratio */
.wide-tile img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}.wide-tile{border-radius:10px;overflow:hidden}

    /* Lightbox styles */
    .lightbox{position:fixed;inset:0;background:rgba(3,6,12,0.85);display:none;align-items:center;justify-content:center;z-index:9999;padding:24px}
    .lightbox.open{display:flex}
    .lightbox-content{max-width:1100px;width:100%;max-height:90vh;display:grid;grid-template-columns:1fr 320px;gap:18px}
    .lightbox-img{background:#000;border-radius:12px;overflow:hidden;display:flex;align-items:center;justify-content:center}
    .lightbox-img img{max-width:100%;max-height:90vh;object-fit:contain;display:block}
    .lightbox-side{color:#eaf4ff}
    .side-actions{display:flex;gap:10px;margin-top:12px}
    .action-btn{display:inline-flex;align-items:center;gap:8px;padding:10px 12px;border-radius:10px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);cursor:pointer}

    @media(max-width:900px){.vertical-gallery{grid-template-columns:repeat(2,1fr)}.lightbox-content{grid-template-columns:1fr}}
    @media(max-width:650px){.hero{grid-template-columns:1fr}.profile-panel{position:static}}
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <div class="card" data-aos="fade-up">
        <h1>{{ person.name }}</h1>
        <div class="subtitle"><span id="typed"></span></div>
        <p class="lead">I build secure systems, perform on stage, and model — tech + creativity.</p>

        <div class="buttons">
          <a class="btn primary" href="{{ person.linkedin }}" target="_blank"><i class="fa-brands fa-linkedin"></i> LinkedIn</a>
          <a class="btn" href="{{ url_for('download_resume') }}" target="_blank"><i class="fa-solid fa-file-arrow-down"></i> Resume</a>
          <a class="btn" href="mailto:{{ person.email }}" class="btn"><i class="fa-solid fa-envelope"></i> Email</a>
          <a class="btn" href="{{ person.youtube }}" target="_blank"><i class="fa-brands fa-youtube"></i> YouTube</a>
          <a class="btn" href="{{ person.instagram }}" target="_blank"><i class="fa-brands fa-instagram"></i> Instagram</a>
        </div>

        <h3 style="margin-top:22px">Projects</h3>
        <div>
          {% for p in person.projects %}
          <p><strong>{{ p.title }}</strong><br><span style="color:var(--muted)">{{ p.desc }}</span></p>
          {% endfor %}
        </div>

        <h3>Certifications</h3>
        <div>
          {% for c in person.certifications %}
          <p><strong>{{ c.title }}</strong><br><span style="color:var(--muted)">{{ c.issuer }}</span></p>
          {% endfor %}
        </div>

        <h3 style="margin-top:22px">Featured Dance Video</h3>
        <a href="{{ person.dance_video_url }}" target="_blank" style="display:block;max-width:360px;border-radius:12px;overflow:hidden;">
          <img src="https://img.youtube.com/vi/{{ person.dance_video_id }}/hqdefault.jpg" style="width:100%;display:block;">
        </a>

        <h3 style="margin-top:26px">Modeling Portfolio</h3>
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

      <aside class="card profile-panel">
        <img src="{{ url_for('static', filename=person.profile_image) }}" alt="Profile">
        <h3>{{ person.name }}</h3>
        <p style="color:var(--muted)">{{ person.title }}</p>
        <div class="buttons" style="justify-content:center;">
          <a class="btn" href="{{ person.linkedin }}" target="_blank"><i class="fa-brands fa-linkedin"></i></a>
          <a class="btn" href="{{ person.youtube }}" target="_blank"><i class="fa-brands fa-youtube"></i></a>
          <a class="btn" href="{{ person.instagram }}" target="_blank"><i class="fa-brands fa-instagram"></i></a>
        </div>
      </aside>
    </div>
  </div>

  <!-- LIGHTBOX MARKUP -->
  <div id="lightbox" class="lightbox" role="dialog" aria-hidden="true">
    <div class="lightbox-content">
      <div class="lightbox-img">
        <img id="lightbox-image" src="" alt="Full image">
      </div>
      <div class="lightbox-side">
        <h3 id="lb-fname">Filename</h3>
        <div class="side-actions">
          <a id="lb-download" class="action-btn" href="#" download><i class="fa-solid fa-arrow-down"></i> Download</a>
          <button id="lb-like" class="action-btn"><i class="fa-regular fa-heart"></i> <span id="lb-like-count">0</span></button>
          <button id="lb-share" class="action-btn"><i class="fa-solid fa-share-nodes"></i> Share</button>
        </div>
        <div style="margin-top:12px;color:var(--muted)">Click outside to close. Likes are stored locally in your browser.</div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
  <script>
    AOS.init({ duration:700, once:true });
    new Typed('#typed',{strings:["{{ person.title }}","Model • Dancer • Cybersecurity","Open to collaborations"],typeSpeed:36,backSpeed:25,loop:true});

    // LIGHTBOX LOGIC
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
      // load likes from localStorage
      const likes = JSON.parse(localStorage.getItem('img_likes')||'{}');
      const count = likes[filename]||0;
      lbLikeCount.textContent = count;
      lbLike.dataset.file = filename;
      lbShare.dataset.file = filename;
    }

    function closeLightbox(){
      lightbox.classList.remove('open');
      lightbox.setAttribute('aria-hidden', 'true');
      lbImage.src = '';
    }

    // attach click on all gallery tiles
    document.querySelectorAll('.vertical-tile, .wide-tile').forEach(tile=>{
      tile.addEventListener('click', ()=>{
        const src = tile.dataset.full || tile.querySelector('img').src;
        const fname = tile.dataset.fname || src.split('/').pop();
        openLightbox(src, fname);
      });
    });

    // close when clicking outside content
    lightbox.addEventListener('click', (e)=>{ if(e.target===lightbox) closeLightbox(); });

    // like button
    lbLike.addEventListener('click', ()=>{
      const file = lbLike.dataset.file;
      const likes = JSON.parse(localStorage.getItem('img_likes')||'{}');
      likes[file] = (likes[file]||0) + 1;
      localStorage.setItem('img_likes', JSON.stringify(likes));
      lbLikeCount.textContent = likes[file];
      // toggle heart icon to filled
      lbLike.innerHTML = '<i class="fa-solid fa-heart" style="color:#ff6b81"></i> ' + '<span id="lb-like-count">'+likes[file]+'</span>';
    });

    // share button: use Web Share API if available, else copy link
    lbShare.addEventListener('click', async ()=>{
      const file = lbShare.dataset.file;
      const url = location.origin + '/static/' + file;
      if(navigator.share){
        try{ await navigator.share({title: 'Image - ' + file, url}); }
        catch(err){ console.log('Share cancelled', err); }
      } else {
        // fallback: copy to clipboard
        try{ await navigator.clipboard.writeText(url); alert('Image URL copied to clipboard'); }
        catch(e){ prompt('Copy this URL', url); }
      }
    });

    // download already wired via anchor

  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML, person=PERSON)

@app.route('/resume')
def download_resume():
    resume_path = os.path.join(app.static_folder or 'static', PERSON["resume_filename"])
    if os.path.exists(resume_path):
        return send_from_directory(app.static_folder or 'static', PERSON["resume_filename"], as_attachment=True)
    abort(404)

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(debug=True)
