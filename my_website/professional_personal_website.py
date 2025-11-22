"""
Single-file Flask app for a professional personal website with animations,
LinkedIn link and resume download.

How to use:
1. Save this file as professional_personal_website.py
2. Create a folder named `static` in the same directory and place your resume as `resume.pdf` and your profile photo as `profile.jpg` (or change filenames in the HTML).
3. Install Flask: pip install Flask
4. Run: python professional_personal_website.py
5. Open http://127.0.0.1:5000 in your browser

This example uses CDN resources (AOS for on-scroll animation, Typed.js for typing effect,
and Font Awesome for icons) to provide a modern animated feel without complicated build steps.

Customize the HTML/CSS (colors, fonts, sections) to match your branding.
"""
from flask import Flask, render_template_string, send_from_directory, abort, url_for
import os

app = Flask(__name__)

# Basic config - change these to your actual info
PERSON = {
    "name": "THARUN R",
    "title": "Software Engineer • CYBER SECURITY Enthusiast",
    "linkedin": "https://www.linkedin.com/in/tharun021/",
    "email": "tharunr2121@gmail.com",
    # location of profile image and resume are expected in ./static/
    "profile_image": "profile.jpg",
    "resume_filename": "resume.pdf",
}

INDEX_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ person.name }} — {{ person.title }}</title>

  <!-- AOS (Animate on Scroll) -->
  <link href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" rel="stylesheet">
  <!-- Typed.js for the title typing effect -->
  <script src="https://cdn.jsdelivr.net/npm/typed.js@2.0.12"></script>
  <!-- Font Awesome for icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

  <style>
    :root{
      --bg: #0f1724;
      --panel: #0b1220;
      --accent: #6ee7b7;
      --muted: #9aa4b2;
      --glass: rgba(255,255,255,0.04);
      --card-shadow: 0 8px 30px rgba(2,6,23,0.6);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }
    html,body{height:100%;margin:0;background:linear-gradient(180deg,#071124 0%, #07182a 60%);color:#e6eef6}
    .container{max-width:1100px;margin:40px auto;padding:28px}

    /* Hero */
    .hero{display:grid;grid-template-columns:1fr 360px;gap:28px;align-items:center}
    .card{background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));border-radius:16px;padding:28px;box-shadow:var(--card-shadow);backdrop-filter: blur(6px)}

    h1{font-size:34px;margin:0 0 8px}
    .subtitle{color:var(--muted);margin-bottom:18px}

    .buttons{display:flex;gap:12px;margin-top:18px}
    .btn{display:inline-flex;gap:10px;align-items:center;padding:10px 14px;border-radius:10px;border:1px solid rgba(255,255,255,0.06);text-decoration:none;color:inherit;background:var(--glass);transition:transform .18s ease, box-shadow .18s ease}
    .btn:hover{transform:translateY(-4px);box-shadow:0 10px 30px rgba(0,0,0,0.6)}
    .btn.primary{background:linear-gradient(90deg, rgba(110,231,183,0.12), rgba(110,231,183,0.06));border:1px solid rgba(110,231,183,0.14)}

    .profile-panel{text-align:center}
    .profile-panel img{width:160px;height:160px;border-radius:20px;object-fit:cover;border:4px solid rgba(255,255,255,0.04)}
    .small{font-size:13px;color:var(--muted)}

    /* Sections */
    section{margin-top:34px}
    .grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
    .skill{padding:18px;border-radius:12px;background:linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.005));}

    footer{margin-top:36px;text-align:center;color:var(--muted);font-size:13px}

    /* Responsive */
    @media (max-width:920px){.hero{grid-template-columns:1fr;}.profile-panel{order:-1;margin-bottom:18px}}
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <div class="card" data-aos="fade-up">
        <h1>{{ person.name }}</h1>
        <div class="subtitle">
          <span id="typed" class="typed"></span>
        </div>

        <p class="small">I build clean, scalable software and enjoy converting ideas into delightful, production-ready products. I have experience with backend systems, machine learning pipelines, and modern frontend stacks. Let's connect 👇</p>

        <div class="buttons">
          <a class="btn primary" href="{{ person.linkedin }}" target="_blank" rel="noopener noreferrer">
            <i class="fa-brands fa-linkedin"></i> View LinkedIn
          </a>

          <a class="btn" href="{{ url_for('download_resume') }}" target="_blank">
            <i class="fa-solid fa-file-arrow-down"></i> Download Resume
          </a>

          <a class="btn" href="mailto:{{ person.email }}">
            <i class="fa-solid fa-envelope"></i> Email
          </a>
        </div>

        <section data-aos="fade-up" data-aos-delay="80">
          <h3 style="margin-top:20px">Selected Projects</h3>
          <div class="grid-3" style="margin-top:12px">
            <div class="skill" data-aos="zoom-in" data-aos-delay="120">
              <strong>Project A</strong>
              <div class="small">Scalable REST API for analytics pipelines.</div>
            </div>
            <div class="skill" data-aos="zoom-in" data-aos-delay="160">
              <strong>Project B</strong>
              <div class="small">End-to-end ML deployment with monitoring.</div>
            </div>
            <div class="skill" data-aos="zoom-in" data-aos-delay="200">
              <strong>Project C</strong>
              <div class="small">Interactive data visualizations and dashboards.</div>
            </div>
          </div>
        </section>

      </div> <!-- end left card -->

      <aside class="card profile-panel" data-aos="fade-left">
        <img src="{{ url_for('static', filename=person.profile_image) }}" alt="Profile">
        <h3 style="margin:14px 0 6px">{{ person.name }}</h3>
        <div class="small">{{ person.title }}</div>

        <div style="margin-top:14px">
          <!-- quick links -->
          <a class="btn" href="{{ person.linkedin }}" target="_blank"><i class="fa-brands fa-linkedin"></i></a>
          <a class="btn" href="{{ url_for('download_resume') }}" target="_blank"><i class="fa-solid fa-file-pdf"></i></a>
        </div>

        <div style="margin-top:18px;text-align:left">
          <h4 style="margin:0 0 8px">Skills</h4>
          <div class="small">Python • Flask • Docker • SQL • PyTorch • React</div>
        </div>
      </aside>
    </div> <!-- hero -->

    <section data-aos="fade-up">
      <div class="card">
        <h3>About me</h3>
        <p class="small">I'm a results-oriented engineer who cares about building maintainable systems, great UX, and shipping quality work. I enjoy mentoring, code reviews, and working with cross-functional teams to bring high-impact products to life.</p>
      </div>
    </section>

    <footer>
      <div>Made with ❤️ • <a href="{{ person.linkedin }}" target="_blank" style="color:inherit;text-decoration:underline">Connect on LinkedIn</a></div>
    </footer>

  </div> <!-- container -->

  <!-- Scripts -->
  <script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
  <script>
    AOS.init({ duration: 700, once: true, easing: 'ease-out-back' });

    // Typed.js initialization for the subtle typographic animation
    document.addEventListener('DOMContentLoaded', function(){
      var typed = new Typed('#typed', {
        strings: ["{{ person.title }}", "Open to remote roles", "Available for consulting"],
        typeSpeed: 40,
        backSpeed: 25,
        backDelay: 1800,
        loop: true
      });
    });
  </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(INDEX_HTML, person=PERSON)


@app.route('/resume')
def download_resume():
    # Serve resume from the static folder. Make sure file exists.
    resume_path = os.path.join(app.static_folder or 'static', PERSON['resume_filename'])
    if os.path.exists(resume_path):
        return send_from_directory(app.static_folder or 'static', PERSON['resume_filename'], as_attachment=True)
    else:
        abort(404, description='Resume not found. Put your resume in the static/ folder and name it "{}".'.format(PERSON['resume_filename']))


if __name__ == '__main__':
    # Create static folder hint (won't overwrite)
    os.makedirs('static', exist_ok=True)
    print("Starting app. Put your resume as static/{} and profile image as static/{}".format(PERSON['resume_filename'], PERSON['profile_image']))
    app.run(debug=True)
