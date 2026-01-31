import base64
import os

def image_to_base64(path):
    with open(path, "rb") as image_file:
        ext = os.path.splitext(path)[1][1:]
        if ext == 'jpg': ext = 'jpeg'
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/{ext};base64,{encoded_string}"

images = [
    "c:/Users/Ryzen 9 5900X/Desktop/Antigravity/el-dorado-site/public/silver-0.png",
    "c:/Users/Ryzen 9 5900X/Desktop/Antigravity/el-dorado-site/public/silver-1.jpg",
    "c:/Users/Ryzen 9 5900X/Desktop/Antigravity/el-dorado-site/public/silver-2.png",
    "c:/Users/Ryzen 9 5900X/Desktop/Antigravity/el-dorado-site/public/silver-3.png"
]

b64_images = [image_to_base64(img) for img in images]

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EL DORADO | Shareable Preview</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Inter:wght@200;300;400&display=swap');
        
        :root {{
            --obsidian: #0A0A0A;
            --off-white: #FAF9F6;
            --aura-gold: #D4AF37;
            --pure-silver: #E5E4E2;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.1);
            --font-serif: 'Cormorant Garamond', serif;
            --font-sans: 'Inter', sans-serif;
        }}

        body {{
            margin: 0;
            background: var(--obsidian);
            color: var(--off-white);
            font-family: var(--font-sans);
            overflow-x: hidden;
        }}

        nav {{
            position: fixed;
            top: 0;
            width: 100%;
            height: 80px;
            display: flex;
            align-items: center;
            background: rgba(10, 10, 10, 0.5);
            backdrop-filter: blur(10px);
            z-index: 100;
            border-bottom: 1px solid var(--glass-border);
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            width: 100%;
        }}

        .nav-content {{
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: center;
        }}

        .brand-logo {{
            font-family: var(--font-serif);
            font-size: 2rem;
            letter-spacing: 0.3em;
            text-decoration: none;
            color: white;
        }}

        #hero {{
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            position: relative;
        }}

        .hero-title {{
            font-family: var(--font-serif);
            font-size: clamp(3rem, 8vw, 6rem);
            margin: 0;
            color: var(--pure-silver);
            letter-spacing: 0.1em;
        }}

        .product-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 3rem;
            padding: 8rem 0;
        }}

        .product-card {{
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            padding: 2rem;
            transition: 0.4s ease;
        }}

        .product-card:hover {{
            border-color: var(--aura-gold);
            transform: translateY(-10px);
        }}

        .product-image {{
            width: 100%;
            aspect-ratio: 1;
            background: rgba(255,255,255,0.02);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}

        .product-image img {{
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
        }}

        .product-title {{
            font-family: var(--font-serif);
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }}

        .product-desc {{
            font-size: 0.8rem;
            opacity: 0.6;
            margin-bottom: 2rem;
            line-height: 1.6;
        }}

        .inquire-btn {{
            display: inline-block;
            border: 1px solid white;
            padding: 0.8rem 2rem;
            font-size: 0.7rem;
            letter-spacing: 0.2em;
            text-decoration: none;
            color: white;
            transition: 0.3s;
        }}

        .inquire-btn:hover {{
            background: white;
            color: black;
        }}
    </style>
</head>
<body>
    <nav>
        <div class="container nav-content">
            <div></div>
            <a href="#" class="brand-logo">EL DORADO</a>
            <div></div>
        </div>
    </nav>

    <section id="hero">
        <h1 class="hero-title">LUNAR ELEGANCE</h1>
        <p style="letter-spacing: 0.5em; opacity: 0.5; margin-top: 1rem;">963HZ SILVER COLLECTION</p>
    </section>

    <div class="container">
        <div class="product-grid">
            <div class="product-card">
                <div class="product-image"><img src="{b64_images[0]}" alt="Lunar Heavy Cuban"></div>
                <h3 class="product-title">Lunar Heavy Cuban</h3>
                <p class="product-desc">Forged in 925 sterling silver, this cuban link resonates with high-frequency clarity.</p>
                <a href="mailto:contact@eldorado.com" class="inquire-btn">INQUIRE</a>
            </div>
            <div class="product-card">
                <div class="product-image"><img src="{b64_images[1]}" alt="Celestial Tennis"></div>
                <h3 class="product-title">Celestial Tennis Chain</h3>
                <p class="product-desc">A continuous stream of light. Meticulously set to reflect the lunar spectrum.</p>
                <a href="mailto:contact@eldorado.com" class="inquire-btn">INQUIRE</a>
            </div>
            <div class="product-card">
                <div class="product-image"><img src="{b64_images[2]}" alt="Resonant Link"></div>
                <h3 class="product-title">Resonant Link Bracelet</h3>
                <p class="product-desc">Fluidity meeting structural perfection. Liquid silver around the wrist.</p>
                <a href="mailto:contact@eldorado.com" class="inquire-btn">INQUIRE</a>
            </div>
            <div class="product-card">
                <div class="product-image"><img src="{b64_images[3]}" alt="Architectural Band"></div>
                <h3 class="product-title">Architectural Silver Band</h3>
                <p class="product-desc">The geometric root of elegance. A bold, architectural take on the classic silver chain.</p>
                <a href="mailto:contact@eldorado.com" class="inquire-btn">INQUIRE</a>
            </div>
        </div>
    </div>
</body>
</html>"""

with open("c:/Users/Ryzen 9 5900X/Desktop/Antigravity/EL_DORADO_SHAREABLE_PREVIEW.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Standalone HTML generated successfully with embedded images.")
