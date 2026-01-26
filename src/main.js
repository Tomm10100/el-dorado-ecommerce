import './style.css'
import { ShoppingCart } from './cart.js'

// Initialize cart - This is already done at the bottom of cart.js
// but we import it here for the type/instance if needed.
// window.cart is already available.

// Initial UI Structure
document.querySelector('#app').innerHTML = `
  <div id="experience-overlay" class="experience-overlay active flex-center">
    <div class="overlay-content">
      <h2 class="serif">963Hz SILVER</h2>
      <button id="enter-btn" class="enter-btn sans">ENTER THE RESONANCE</button>
      <p class="sans" style="opacity: 0.4; font-size: 0.6rem; margin-top: 1rem; letter-spacing: 0.2em;">SOUND RECOMMENDED</p>
    </div>
  </div>

  <nav id="top-nav">
    <button id="mobile-menu-btn" class="mobile-menu-btn sans">☰</button>
    <div class="container nav-content">
      <div class="nav-links sans desktop-nav">
        <a href="#shop">SHOP</a>
        <a href="#collections">RESEARCH</a>
      </div>
      <div class="logo-container serif">
        <a href="/" class="brand-logo">EL DORADO</a>
      </div>
      <div class="nav-links sans desktop-nav">
        <a href="#about">ABOUT</a>
        <button id="cart-btn" class="cart-btn glass">
          CART <span id="cart-count"></span>
        </button>
      </div>
    </div>
    <div id="mobile-menu" class="mobile-menu glass">
      <a href="#shop">SHOP</a>
      <a href="#collections">RESEARCH</a>
      <a href="#about">ABOUT</a>
      <button id="cart-btn-mobile" class="cart-btn-mobile">
        CART (<span id="cart-count-mobile">0</span>)
      </button>
      <a href="mailto:tommy@innovlead.ca">CONTACT</a>
    </div>
  </nav>

  <main>
    <section id="hero" class="flex-center">
      <div class="frequency-controls">
        <div class="frequency-display">
          <span class="freq-label">Current Resonance</span>
          <span class="freq-value">963Hz</span>
          <button id="resonance-toggle" class="resonance-toggle sans">
            <span class="pulse-icon"></span>
            ACTIVE RESONANCE
          </button>
        </div>
      </div>
      
      <div id="hero-ring-container" class="hero-visual"></div>

      <div id="visual-affirmation" class="visual-affirmation sans"></div>

      <div class="hero-copy">
        <h1 class="serif">LUNAR ELEGANCE</h1>
        <p class="sans">The Initial Silver Collection</p>
      </div>

      <div id="resonance-visualizer"></div>
    </section>

    <section id="collections" class="section-padding">
      <div class="container">
        <h2 class="serif" style="text-align: center; font-size: 3rem; margin-bottom: 6rem;">THE SILVER COLLECTION</h2>
        <div id="product-grid" class="product-grid"></div>
      </div>
    </section>
  </main>

  <footer class="section-padding" style="text-align: center; border-top: 1px solid rgba(255,255,255,0.05);">
    <p class="sans" style="font-size: 0.7rem; letter-spacing: 0.3em; opacity: 0.4;">&copy; 2025 EL DORADO. V2.0 - COSMIC UPDATE LIVE.</p>
  </footer>
`

// Product Data with Prices - UPDATED WITH ACTUAL INVENTORY
const PRODUCTS = [
  {
    id: 0,
    name: "Cruz-Ki",
    price: 200,
    desc: "Stunning channel-set cross pendant featuring brilliant green and white cubic zirconia stones. Each stone is meticulously placed in premium sterling silver, creating a striking contrast that catches light from every angle. A powerful symbol of faith meets luxury craftsmanship.",
    img: "/product-pendant.jpg",
    category: "pendant",
    resonance: "963Hz"
  },
  {
    id: 1,
    name: "Fuego Cadena",
    price: 1200,
    desc: "Luxury 22-inch Cuban link chain featuring invisible-set zirconia stones that create a seamless fire of brilliance. Crafted in premium sterling silver with a special box lock clasp for ultimate security. Each link is precision-engineered to showcase maximum sparkle while maintaining exceptional durability.",
    img: "/product-chain.jpg",
    category: "chain",
    resonance: "963Hz"
  },
  {
    id: 2,
    name: "Dumfe",
    price: 400,
    desc: "8-inch Cuban link bracelet featuring invisible-set cubic zirconia stones in premium sterling silver. Each stone is precision-placed to create a seamless display of brilliance. Secured with a special box lock clasp for ultimate security and elegance.",
    img: "/product-bracelet-1.jpg",
    category: "bracelet",
    resonance: "963Hz"
  },
  {
    id: 3,
    name: "Chan",
    price: 300,
    desc: "Handmade by humans, for humans. Exquisite 7-8 inch Gucci link bracelet crafted in 925 sterling silver. Each link is meticulously shaped by skilled artisans, creating a timeless piece that celebrates authentic craftsmanship and human artistry.",
    img: "/product-bracelet-2.jpg",
    category: "bracelet",
    resonance: "963Hz"
  },
  {
    id: 4,
    name: "Oni",
    price: 200,
    desc: "Handmade for humans, by humans. Bold box chain bracelet crafted in 925 sterling silver. Each link is individually shaped by master artisans, creating a piece that embodies strength and authenticity. A statement of pure craftsmanship.",
    img: "/product-bracelet-3.jpg",
    category: "bracelet",
    resonance: "963Hz"
  },
  {
    id: 5,
    name: "Fan",
    price: 200,
    desc: "Handmade by humans, for humans. Elegant 7-8 inch chain link bracelet in 925 sterling silver. Each link is carefully crafted by skilled artisans, creating a fluid, timeless design that flows naturally with your movement.",
    img: "/product-bracelet-4.jpg",
    category: "bracelet",
    resonance: "963Hz"
  }
];

function initHero() {
  const container = document.querySelector('#hero-ring-container');
  const img = document.createElement('img');
  img.src = '/product-chain.jpg'; // Using the iced chain for hero
  img.className = 'hero-primary-visual';
  container.appendChild(img);

  window.addEventListener('mousemove', (e) => {
    const x = (e.clientX / window.innerWidth - 0.5) * 30;
    const y = (e.clientY / window.innerHeight - 0.5) * 30;
    img.style.transform = `translate(${x}px, ${y}px) rotate(${x / 10}deg)`;
  });
}

function initVisualizer() {
  const visualizer = document.querySelector('#resonance-visualizer');
  visualizer.innerHTML = ''; // Clear existing
  const barCount = 60; // More bars for more impact

  for (let i = 0; i < barCount; i++) {
    const bar = document.createElement('div');
    bar.className = 'wave-bar';
    visualizer.appendChild(bar);
  }

  function animate() {
    const bars = document.querySelectorAll('.wave-bar');
    const time = Date.now() * 0.003;

    bars.forEach((bar, i) => {
      // Create a more complex wave pattern
      const multiplier = audioEngine.isPlaying ? 2.5 : 1;
      const wave1 = Math.sin(time + i * 0.2) * (40 * multiplier);
      const wave2 = Math.sin(time * 0.5 + i * 0.1) * (20 * multiplier);
      const noise = Math.random() * 15;

      const h = 10 + Math.abs(wave1 + wave2 + noise);
      bar.style.height = `${h}px`;

      // Dynamic opacity and glow based on height
      const intensity = h / 80;
      bar.style.opacity = 0.3 + (intensity * 0.7);

      // Color shift between silver and gold
      if (intensity > 0.7) {
        bar.style.background = 'var(--aura-gold)';
        bar.style.boxShadow = '0 0 20px var(--aura-gold)';
      } else {
        bar.style.background = 'var(--pure-silver)';
        bar.style.boxShadow = 'none';
      }
    });
    requestAnimationFrame(animate);
  }
  animate();
}

function renderProducts() {
  const grid = document.querySelector('#product-grid');
  grid.innerHTML = PRODUCTS.map((p, index) => {
    // Determine card size/style based on index for a dynamic layout
    const isLarge = index % 3 === 0;
    const variantClass = isLarge ? 'product-card-large' : 'product-card-standard';

    return `
      <div class="product-card glass ${variantClass}" data-aos="fade-up" style="--delay: ${index * 0.1}s">
        <div class="product-image-container">
          <img src="${p.img}" alt="${p.name}" class="parallax-img">
          <div class="demo-badge">DEMO</div>
          <div class="product-resonance-overlay sans">${p.resonance} RESONANCE</div>
        </div>
        <div class="product-info">
          <div class="product-header">
            <h3 class="product-title serif">${p.name}</h3>
            <span class="product-price sans">$${p.price}</span>
          </div>
          <p class="product-desc sans">${p.desc}</p>
          <div class="product-footer">
            <button class="add-to-cart-btn-premium sans" data-product-id="${p.id}">
              <span class="btn-icon">🛒</span>
              <span class="btn-text">ADD TO COLLECTION</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');

  // Add event listeners to cart buttons with enhanced feedback
  document.querySelectorAll('.add-to-cart-btn-premium').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const button = e.currentTarget;
      const productId = parseInt(button.getAttribute('data-product-id'));
      const product = PRODUCTS.find(p => p.id === productId);

      if (product && window.cart) {
        window.cart.addItem(product);

        // Visual feedback
        const originalText = button.innerHTML;
        button.innerHTML = '✓ ADDED!';
        button.style.background = 'linear-gradient(135deg, #00ff88, #00cc66)';
        button.style.transform = 'scale(0.95)';

        setTimeout(() => {
          button.innerHTML = originalText;
          button.style.background = '';
          button.style.transform = '';
        }, 1500);
      }
    });
  });
}

function initMobileMenu() {
  const menuBtn = document.querySelector('#mobile-menu-btn');
  const mobileMenu = document.querySelector('#mobile-menu');

  menuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('active');
  });

  // Close menu when clicking a link
  document.querySelectorAll('#mobile-menu a').forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.classList.remove('active');
    });
  });
}

function initCartButtons() {
  // Desktop cart button
  const cartBtn = document.querySelector('#cart-btn');
  if (cartBtn) {
    cartBtn.addEventListener('click', () => {
      window.cart.openCart();
    });
  }

  // Mobile cart button
  const cartBtnMobile = document.querySelector('#cart-btn-mobile');
  if (cartBtnMobile) {
    cartBtnMobile.addEventListener('click', () => {
      document.querySelector('#mobile-menu').classList.remove('active');
      window.cart.openCart();
    });
  }

  // Sync cart counts
  const syncCounts = () => {
    const count = window.cart.getItemCount();
    const mobileBadge = document.querySelector('#cart-count-mobile');
    if (mobileBadge) {
      mobileBadge.textContent = count;
    }
  };

  // Update counts periodically
  setInterval(syncCounts, 500);
}

function initNavHighlight() {
  const nav = document.querySelector('#top-nav');
  window.addEventListener('scroll', () => {
    nav.style.background = window.scrollY > 50 ? 'rgba(10,10,10,0.9)' : 'transparent';
    nav.style.height = window.scrollY > 50 ? '60px' : '80px';
  });
}

// Resonance Audio Engine (Professional Real-File Edition)
class ResonanceEngine {
  constructor() {
    this.audioCtx = null;
    this.source = null;
    this.audioElement = null;
    this.masterFilter = null;
    this.masterGain = null;
    this.isPlaying = false;
    this.bpm = 124;
    this.audioUrl = '/afro-house-loop.mp3'; // Local Afro-House Loop
  }

  init() {
    this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    this.audioElement = new Audio(this.audioUrl);
    this.audioElement.loop = true;
    this.audioElement.crossOrigin = "anonymous";

    this.source = this.audioCtx.createMediaElementSource(this.audioElement);

    // DJ Master Filter (Luxury Depth)
    this.masterFilter = this.audioCtx.createBiquadFilter();
    this.masterFilter.type = 'lowpass';
    this.masterFilter.frequency.setValueAtTime(400, this.audioCtx.currentTime); // Start muffled
    this.masterFilter.Q.setValueAtTime(1.5, this.audioCtx.currentTime);

    this.masterGain = this.audioCtx.createGain();
    this.masterGain.gain.setValueAtTime(0, this.audioCtx.currentTime);

    this.source.connect(this.masterFilter);
    this.masterFilter.connect(this.masterGain);
    this.masterGain.connect(this.audioCtx.destination);

    // Rhythmic UI Pulse Logic (Synchronized to BPM)
    this.startRhythmicPulse();
  }

  startRhythmicPulse() {
    const beatInterval = (60 / this.bpm) * 1000;
    setInterval(() => {
      if (!this.isPlaying) return;
      const logo = document.querySelector('.brand-logo');
      if (logo) {
        logo.classList.add('kick-pulse');
        setTimeout(() => logo.classList.remove('kick-pulse'), 150);
      }
    }, beatInterval);
  }

  openFilter() {
    if (!this.masterFilter) return;
    const time = this.audioCtx.currentTime;
    this.masterFilter.frequency.exponentialRampToValueAtTime(3000, time + 2);
  }

  closeFilter() {
    if (!this.masterFilter) return;
    const time = this.audioCtx.currentTime;
    this.masterFilter.frequency.exponentialRampToValueAtTime(400, time + 4);
  }

  start() {
    if (!this.audioCtx) this.init();
    if (this.audioCtx.state === 'suspended') this.audioCtx.resume();

    this.audioElement.play();
    this.masterGain.gain.linearRampToValueAtTime(0.8, this.audioCtx.currentTime + 2);
    this.isPlaying = true;
  }

  stop() {
    if (this.masterGain) {
      this.masterGain.gain.linearRampToValueAtTime(0, this.audioCtx.currentTime + 1);
      setTimeout(() => this.audioElement.pause(), 1000);
    }
    this.isPlaying = false;
  }
}

const audioEngine = new ResonanceEngine();

// Visual Typographic Journey
class VisualJourney {
  constructor() {
    this.affirmations = [
      "YOUR FREQUENCY DEFINES YOUR REALITY",
      "ABUNDANCE FLOWS THROUGH YOU LIKE LIQUID GOLD",
      "RADIATE HEALTH • VIBRATE LOVE • BECOME THE LIGHT",
      "EVERYTHING YOU SEEK IS RESONATING WITHIN YOU"
    ];
    this.container = null;
  }

  init() {
    this.container = document.querySelector('#visual-affirmation');
  }

  start() {
    this.schedule(0, 5000);  // 5s: Identity
    this.schedule(1, 20000); // 20s: Abundance
    this.schedule(2, 40000); // 40s: Health/Love
    this.schedule(3, 60000); // 60s: Peace
  }

  schedule(index, delay) {
    setTimeout(() => {
      this.show(this.affirmations[index]);
    }, delay);
  }

  show(text) {
    if (!this.container) return;
    this.container.textContent = text;
    this.container.classList.add('active');

    // DJ Filter Sweep: Open up the sound for the truth
    audioEngine.openFilter();

    setTimeout(() => {
      this.container.classList.remove('active');
      audioEngine.closeFilter();
    }, 8000); // More time to absorb the truth
  }
}

const journey = new VisualJourney();

function initAudio() {
  const toggle = document.querySelector('#resonance-toggle');
  const enterBtn = document.querySelector('#enter-btn');
  const overlay = document.querySelector('#experience-overlay');

  const startExperience = () => {
    if (!audioEngine.isPlaying) {
      audioEngine.start();
      toggle.classList.add('active');
      journey.init();
      journey.start();

      // Hide overlay
      overlay.style.opacity = '0';
      setTimeout(() => overlay.remove(), 1000);
    }
  };

  if (enterBtn) {
    enterBtn.addEventListener('click', startExperience);
  }

  if (toggle) {
    toggle.addEventListener('click', () => {
      if (audioEngine.isPlaying) {
        audioEngine.stop();
        toggle.classList.remove('active');
      } else {
        audioEngine.start();
        toggle.classList.add('active');
      }
    });
  }
}

// Kickoff
initHero();
initVisualizer();
renderProducts();
initNavHighlight();
initMobileMenu();
initCartButtons();
initAudio();
