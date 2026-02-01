(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const i of document.querySelectorAll('link[rel="modulepreload"]'))s(i);new MutationObserver(i=>{for(const a of i)if(a.type==="childList")for(const o of a.addedNodes)o.tagName==="LINK"&&o.rel==="modulepreload"&&s(o)}).observe(document,{childList:!0,subtree:!0});function e(i){const a={};return i.integrity&&(a.integrity=i.integrity),i.referrerPolicy&&(a.referrerPolicy=i.referrerPolicy),i.crossOrigin==="use-credentials"?a.credentials="include":i.crossOrigin==="anonymous"?a.credentials="omit":a.credentials="same-origin",a}function s(i){if(i.ep)return;i.ep=!0;const a=e(i);fetch(i.href,a)}})();const E="modulepreload",C=function(n){return"/"+n},y={},w=function(t,e,s){let i=Promise.resolve();if(e&&e.length>0){let p=function(r){return Promise.all(r.map(d=>Promise.resolve(d).then(u=>({status:"fulfilled",value:u}),u=>({status:"rejected",reason:u}))))};var o=p;document.getElementsByTagName("link");const l=document.querySelector("meta[property=csp-nonce]"),c=l?.nonce||l?.getAttribute("nonce");i=p(e.map(r=>{if(r=C(r),r in y)return;y[r]=!0;const d=r.endsWith(".css"),u=d?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${r}"]${u}`))return;const m=document.createElement("link");if(m.rel=d?"stylesheet":E,d||(m.as="script"),m.crossOrigin="",m.href=r,c&&m.setAttribute("nonce",c),document.head.appendChild(m),d)return new Promise((g,b)=>{m.addEventListener("load",g),m.addEventListener("error",()=>b(new Error(`Unable to preload CSS for ${r}`)))})}))}function a(l){const c=new Event("vite:preloadError",{cancelable:!0});if(c.payload=l,window.dispatchEvent(c),!c.defaultPrevented)throw l}return i.then(l=>{for(const c of l||[])c.status==="rejected"&&a(c.reason);return t().catch(a)})};class T{constructor(){this.items=this.loadCart(),this.init()}init(){this.createCartUI(),this.updateCartCount()}loadCart(){const t=localStorage.getItem("eldorado-cart");return t?JSON.parse(t):[]}saveCart(){localStorage.setItem("eldorado-cart",JSON.stringify(this.items)),this.updateCartCount()}addItem(t){const e=this.items.find(s=>s.id===t.id);e?e.quantity+=1:this.items.push({...t,quantity:1}),this.saveCart(),this.showNotification(`${t.name} added to cart`),this.renderCart(),window.analytics&&window.analytics.trackAddToCart(t)}removeItem(t){this.items=this.items.filter(e=>e.id!==t),this.saveCart(),this.renderCart()}updateQuantity(t,e){const s=this.items.find(i=>i.id===t);s&&(s.quantity=Math.max(1,e),this.saveCart(),this.renderCart())}getTotal(){return this.items.reduce((t,e)=>t+e.price*e.quantity,0)}getItemCount(){return this.items.reduce((t,e)=>t+e.quantity,0)}updateCartCount(){const t=document.querySelector("#cart-count"),e=this.getItemCount();t&&(t.textContent=e,t.style.display=e>0?"flex":"none")}createCartUI(){document.body.insertAdjacentHTML("beforeend",`
      <div id="cart-overlay" class="cart-overlay">
        <div class="cart-sidebar glass">
          <div class="cart-header">
            <h3 class="serif">YOUR CART</h3>
            <button id="close-cart" class="close-btn">&times;</button>
          </div>
          <div id="cart-items" class="cart-items"></div>
          <div class="cart-footer">
            <div class="cart-total">
              <span class="sans">TOTAL:</span>
              <span class="serif" id="cart-total">$0</span>
            </div>
            <button id="checkout-stripe" class="checkout-btn sans">
              CHECKOUT WITH CARD
            </button>
            <button id="checkout-crypto" class="checkout-btn crypto-btn sans">
              PAY WITH XRP
            </button>
          </div>
        </div>
      </div>
    `),document.querySelector("#close-cart").addEventListener("click",()=>this.closeCart()),document.querySelector("#cart-overlay").addEventListener("click",e=>{e.target.id==="cart-overlay"&&this.closeCart()}),document.querySelector("#checkout-stripe").addEventListener("click",()=>this.checkoutStripe()),document.querySelector("#checkout-crypto").addEventListener("click",()=>this.checkoutCrypto())}openCart(){this.renderCart(),document.querySelector("#cart-overlay").classList.add("active"),document.body.style.overflow="hidden"}closeCart(){document.querySelector("#cart-overlay").classList.remove("active"),document.body.style.overflow=""}renderCart(){const t=document.querySelector("#cart-items");if(this.items.length===0){t.innerHTML=`
        <div class="empty-cart sans">
          <p>Your cart is empty</p>
        </div>
      `,document.querySelector("#cart-total").textContent="$0";return}t.innerHTML=this.items.map(e=>`
      <div class="cart-item">
        <img src="${e.img}" alt="${e.name}" class="cart-item-img">
        <div class="cart-item-details">
          <h4 class="serif">${e.name}</h4>
          <p class="sans">$${e.price}</p>
          <div class="quantity-controls">
            <button class="qty-btn" onclick="window.cart.updateQuantity(${e.id}, ${e.quantity-1})">-</button>
            <span class="quantity">${e.quantity}</span>
            <button class="qty-btn" onclick="window.cart.updateQuantity(${e.id}, ${e.quantity+1})">+</button>
          </div>
        </div>
        <button class="remove-btn sans" onclick="window.cart.removeItem(${e.id})">
          &times;
        </button>
      </div>
    `).join(""),document.querySelector("#cart-total").textContent=`$${this.getTotal()}`}async checkoutStripe(){if(this.items.length===0){alert("Your cart is empty");return}const t="pk_test_YOUR_PUBLISHABLE_KEY_HERE";if(t.includes("YOUR_")){alert("Stripe is not configured. Please set VITE_STRIPE_PUBLIC_KEY in .env");return}try{const{loadStripe:e}=await w(async()=>{const{loadStripe:i}=await import("./index-BnH8vN8J.js");return{loadStripe:i}},[]),s=await e(t);window.analytics&&window.analytics.trackInitiateCheckout(this.items,this.getTotal()),this.showNotification("Redirecting to secure checkout..."),alert("Redirecting to Stripe... (Requires Price IDs in production)")}catch(e){console.error("Checkout failed:",e),alert("Unable to initiate checkout. Please try again.")}}checkoutCrypto(){if(this.items.length===0){alert("Your cart is empty");return}this.showCryptoPayment()}showCryptoPayment(){const t=this.getTotal(),e=(t/.5).toFixed(2),s=document.createElement("div");s.className="crypto-modal",s.innerHTML=`
      <div class="crypto-content glass">
        <h3 class="serif">Pay with XRP</h3>
        <div class="crypto-details">
          <p class="sans">Order Total: <strong>$${t} USD</strong></p>
          <p class="sans">XRP Amount: <strong>${e} XRP</strong></p>
          <div class="xrp-address">
            <p class="sans">Send XRP to:</p>
            <code id="xrp-address">rYOUR_XRP_ADDRESS_HERE</code>
            <button class="copy-btn sans" onclick="navigator.clipboard.writeText(document.getElementById('xrp-address').textContent)">
              COPY ADDRESS
            </button>
          </div>
          <p class="sans" style="font-size: 0.75rem; opacity: 0.6; margin-top: 2rem;">
            After sending, email tommy@innovlead.ca with your transaction ID
          </p>
        </div>
        <button class="close-modal-btn sans" onclick="this.parentElement.parentElement.remove()">
          CLOSE
        </button>
      </div>
    `,document.body.appendChild(s)}showNotification(t){const e=document.createElement("div");e.className="cart-notification glass",e.textContent=t,document.body.appendChild(e),setTimeout(()=>e.classList.add("show"),100),setTimeout(()=>{e.classList.remove("show"),setTimeout(()=>e.remove(),300)},2e3)}clear(){this.items=[],this.saveCart(),this.renderCart()}}window.cart=new T;document.querySelector("#app").innerHTML=`
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
    <p class="sans" style="font-size: 0.7rem; letter-spacing: 0.3em; opacity: 0.4;">&copy; 2026 EL DORADO. V2.0 - COSMIC UPDATE LIVE.</p>
  </footer>
`;const v=[{id:0,name:"Cruz-Ki",price:200,desc:"Stunning channel-set cross pendant featuring brilliant green and white cubic zirconia stones. Each stone is meticulously placed in premium sterling silver, creating a striking contrast that catches light from every angle. A powerful symbol of faith meets luxury craftsmanship.",img:"/product-pendant.jpg",category:"pendant",resonance:"963Hz"},{id:1,name:"Fuego Cadena",price:1200,desc:"Luxury 22-inch Cuban link chain featuring invisible-set zirconia stones that create a seamless fire of brilliance. Crafted in premium sterling silver with a special box lock clasp for ultimate security. Each link is precision-engineered to showcase maximum sparkle while maintaining exceptional durability.",img:"/product-chain.jpg",category:"chain",resonance:"963Hz"},{id:2,name:"Dumfe",price:400,desc:"8-inch Cuban link bracelet featuring invisible-set cubic zirconia stones in premium sterling silver. Each stone is precision-placed to create a seamless display of brilliance. Secured with a special box lock clasp for ultimate security and elegance.",img:"/product-bracelet-1.jpg",category:"bracelet",resonance:"963Hz"},{id:3,name:"Chan",price:300,desc:"Handmade by humans, for humans. Exquisite 7-8 inch Gucci link bracelet crafted in 925 sterling silver. Each link is meticulously shaped by skilled artisans, creating a timeless piece that celebrates authentic craftsmanship and human artistry.",img:"/product-bracelet-2.jpg",category:"bracelet",resonance:"963Hz"},{id:4,name:"Oni",price:200,desc:"Handmade for humans, by humans. Bold box chain bracelet crafted in 925 sterling silver. Each link is individually shaped by master artisans, creating a piece that embodies strength and authenticity. A statement of pure craftsmanship.",img:"/product-bracelet-3.jpg",category:"bracelet",resonance:"963Hz"},{id:5,name:"Fan",price:200,desc:"Handmade by humans, for humans. Elegant 7-8 inch chain link bracelet in 925 sterling silver. Each link is carefully crafted by skilled artisans, creating a fluid, timeless design that flows naturally with your movement.",img:"/product-bracelet-4.jpg",category:"bracelet",resonance:"963Hz"}];function S(){const n=document.querySelector("#hero-ring-container"),t=document.createElement("img");t.src="/hero-chain.png",t.className="hero-primary-visual",n.appendChild(t),window.addEventListener("mousemove",e=>{const s=(e.clientX/window.innerWidth-.5)*30,i=(e.clientY/window.innerHeight-.5)*30;window.innerWidth>768&&(t.style.transform=`translate(${s}px, ${i}px) rotate(90deg) rotate(${s/10}deg)`)}),window.innerWidth>768&&(t.style.transform="rotate(90deg)")}function L(){const n=document.querySelector("#resonance-visualizer");n.innerHTML="";const t=60;for(let s=0;s<t;s++){const i=document.createElement("div");i.className="wave-bar",n.appendChild(i)}function e(){const s=document.querySelectorAll(".wave-bar"),i=Date.now()*.003;s.forEach((a,o)=>{const l=h.isPlaying?2.5:1,c=Math.sin(i+o*.2)*(40*l),p=Math.sin(i*.5+o*.1)*(20*l),r=Math.random()*15,d=10+Math.abs(c+p+r);a.style.height=`${d}px`;const u=d/80;a.style.opacity=.3+u*.7,u>.7?(a.style.background="var(--aura-gold)",a.style.boxShadow="0 0 20px var(--aura-gold)"):(a.style.background="var(--pure-silver)",a.style.boxShadow="none")}),requestAnimationFrame(e)}e()}function x(){const n=document.querySelector("#product-grid");n.innerHTML=v.map((t,e)=>`
      <div class="product-card glass ${e%3===0?"product-card-large":"product-card-standard"}" data-aos="fade-up" style="--delay: ${e*.1}s">
        <div class="product-image-container">
          <img src="${t.img}" alt="${t.name}" class="parallax-img">
          <div class="product-resonance-overlay sans">${t.resonance} RESONANCE</div>
        </div>
        <div class="product-info">
          <div class="product-header">
            <h3 class="product-title serif">${t.name}</h3>
            <span class="product-price sans">$${t.price}</span>
          </div>
          <p class="product-desc sans">${t.desc}</p>
          <div class="product-footer">
            <button class="add-to-cart-btn-premium sans" data-product-id="${t.id}">
              <span class="btn-icon">🛒</span>
              <span class="btn-text">ADD TO COLLECTION</span>
            </button>
          </div>
        </div>
      </div>
    `).join(""),document.querySelectorAll(".add-to-cart-btn-premium").forEach(t=>{t.addEventListener("click",e=>{const s=e.currentTarget,i=parseInt(s.getAttribute("data-product-id")),a=v.find(o=>o.id===i);if(a&&window.cart){window.cart.addItem(a);const o=s.innerHTML;s.innerHTML="✓ ADDED!",s.style.background="linear-gradient(135deg, #00ff88, #00cc66)",s.style.transform="scale(0.95)",setTimeout(()=>{s.innerHTML=o,s.style.background="",s.style.transform=""},1500)}})})}function k(){const n=document.querySelector("#mobile-menu-btn"),t=document.querySelector("#mobile-menu");n.addEventListener("click",()=>{t.classList.toggle("active")}),document.querySelectorAll("#mobile-menu a").forEach(e=>{e.addEventListener("click",()=>{t.classList.remove("active")})})}function A(){const n=document.querySelector("#cart-btn");n&&n.addEventListener("click",()=>{window.cart.openCart()});const t=document.querySelector("#cart-btn-mobile");t&&t.addEventListener("click",()=>{document.querySelector("#mobile-menu").classList.remove("active"),window.cart.openCart()}),setInterval(()=>{const s=window.cart.getItemCount(),i=document.querySelector("#cart-count-mobile");i&&(i.textContent=s)},500)}function R(){const n=document.querySelector("#top-nav");window.addEventListener("scroll",()=>{n.style.background=window.scrollY>50?"rgba(10,10,10,0.9)":"transparent",n.style.height=window.scrollY>50?"60px":"80px"})}class q{constructor(){this.audioCtx=null,this.source=null,this.audioElement=null,this.masterFilter=null,this.masterGain=null,this.isPlaying=!1,this.bpm=124,this.audioUrl="/afro-house-loop.mp3"}init(){this.audioCtx=new(window.AudioContext||window.webkitAudioContext),this.audioElement=new Audio(this.audioUrl),this.audioElement.loop=!0,this.audioElement.crossOrigin="anonymous",this.source=this.audioCtx.createMediaElementSource(this.audioElement),this.masterFilter=this.audioCtx.createBiquadFilter(),this.masterFilter.type="lowpass",this.masterFilter.frequency.setValueAtTime(400,this.audioCtx.currentTime),this.masterFilter.Q.setValueAtTime(1.5,this.audioCtx.currentTime),this.masterGain=this.audioCtx.createGain(),this.masterGain.gain.setValueAtTime(0,this.audioCtx.currentTime),this.source.connect(this.masterFilter),this.masterFilter.connect(this.masterGain),this.masterGain.connect(this.audioCtx.destination),this.startRhythmicPulse()}startRhythmicPulse(){const t=60/this.bpm*1e3;setInterval(()=>{if(!this.isPlaying)return;const e=document.querySelector(".brand-logo");e&&(e.classList.add("kick-pulse"),setTimeout(()=>e.classList.remove("kick-pulse"),150))},t)}openFilter(){if(!this.masterFilter)return;const t=this.audioCtx.currentTime;this.masterFilter.frequency.exponentialRampToValueAtTime(3e3,t+2)}closeFilter(){if(!this.masterFilter)return;const t=this.audioCtx.currentTime;this.masterFilter.frequency.exponentialRampToValueAtTime(400,t+4)}start(){this.audioCtx||this.init(),this.audioCtx.state==="suspended"&&this.audioCtx.resume(),this.audioElement.play(),this.masterGain.gain.linearRampToValueAtTime(.8,this.audioCtx.currentTime+2),this.isPlaying=!0}stop(){this.masterGain&&(this.masterGain.gain.linearRampToValueAtTime(0,this.audioCtx.currentTime+1),setTimeout(()=>this.audioElement.pause(),1e3)),this.isPlaying=!1}}const h=new q;class O{constructor(){this.affirmations=["YOUR FREQUENCY DEFINES YOUR REALITY","ABUNDANCE FLOWS THROUGH YOU LIKE LIQUID GOLD","RADIATE HEALTH • VIBRATE LOVE • BECOME THE LIGHT","EVERYTHING YOU SEEK IS RESONATING WITHIN YOU"],this.container=null}init(){this.container=document.querySelector("#visual-affirmation")}start(){this.schedule(0,5e3),this.schedule(1,2e4),this.schedule(2,4e4),this.schedule(3,6e4)}schedule(t,e){setTimeout(()=>{this.show(this.affirmations[t])},e)}show(t){this.container&&(this.container.textContent=t,this.container.classList.add("active"),h.openFilter(),setTimeout(()=>{this.container.classList.remove("active"),h.closeFilter()},8e3))}}const f=new O;function I(){const n=document.querySelector("#resonance-toggle"),t=document.querySelector("#enter-btn"),e=document.querySelector("#experience-overlay"),s=()=>{h.isPlaying||(h.start(),n.classList.add("active"),f.init(),f.start(),e.style.opacity="0",setTimeout(()=>e.remove(),1e3))};t&&t.addEventListener("click",s),n&&n.addEventListener("click",()=>{h.isPlaying?(h.stop(),n.classList.remove("active")):(h.start(),n.classList.add("active"))})}S();L();x();R();k();A();I();
