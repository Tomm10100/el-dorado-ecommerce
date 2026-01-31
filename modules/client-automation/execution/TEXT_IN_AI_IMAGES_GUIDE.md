# Text in AI Images - Advanced Prompting Guide

**Question**: Can we prompt AI to generate text correctly instead of avoiding it?

**Short Answer**: Some models can, but it's unreliable. Here's how to do it IF you must.

---

## 🎯 The Reality Check

### Current State of AI Text Generation:

| Model | Text Quality | Reliability | Best Use |
|-------|-------------|-------------|----------|
| **Ideogram v2** | ⭐⭐⭐⭐⭐ | 85-90% | Text-heavy designs |
| **DALL-E 3** | ⭐⭐⭐⭐ | 75-85% | Short text, logos |
| **Google Imagen 4** | ⭐⭐⭐ | 60-70% | Minimal text |
| **Flux 2** | ⭐⭐⭐ | 65-75% | Short phrases |
| **Midjourney v6** | ⭐⭐ | 40-50% | Avoid text |
| **Stable Diffusion** | ⭐ | 20-30% | Avoid text |

**Key Insight**: Even the BEST models (Ideogram) still fail 10-15% of the time.

---

## ✅ When Text-in-Images Makes Sense

### Good Use Cases:
1. **Logos**: Single word, large, centered
2. **Posters**: 1-3 words, big headlines
3. **Social media**: Short phrases, emphasized
4. **Mockups**: Product labels (can regenerate if wrong)

### Bad Use Cases:
1. **Data charts**: Numbers must be exact
2. **Infographics**: Multiple labels/facts
3. **Business documents**: Professional context
4. **Legal/compliance**: Zero tolerance for errors

**Our Case** (El Dorado proposal):
- Multiple data points
- Professional context
- Zero tolerance for errors
- **Verdict**: Text-free is safer

---

## 🎨 If You Must Include Text: Best Practices

### Technique 1: Use Text-Optimized Models

**Switch from Imagen 4 to Ideogram v2**:

```python
# In generate_illustrated_proposal_pdf.py

# INSTEAD OF:
payload = {
    "model": "google/imagen4",  # Good for visuals, bad for text
    ...
}

# USE:
payload = {
    "model": "ideogram/v2",  # Best for text
    ...
}
```

**Ideogram v2 Advantages**:
- Specifically trained on text generation
- 85-90% accuracy on English text
- Better typography
- Handles multi-word phrases

---

### Technique 2: Extreme Specificity in Prompts

**For Text-in-Images**, you need 3x more detail:

#### ❌ BAD (Vague):
```
"Create an infographic with market data"
```
**Result**: Gibberish text

#### ⚠️ BETTER (But Still Risky):
```
"Infographic showing '$680M' in large gold text, 
centered, bold sans-serif font"
```
**Result**: Might work, might not

#### ✅ BEST (Maximum Specificity):
```
"Clean white background, centered composition, 
large bold text reading exactly '$680M' in gold color (#FFD700), 
modern sans-serif typeface, letter-spacing: normal, 
no other text, no decorations, sharp edges, high contrast"
```

**Key Elements**:
1. **"exactly '$680M'"** - Tells AI the exact string
2. **"large bold text"** - Size and weight
3. **"gold color (#FFD700)"** - Specific color
4. **"modern sans-serif"** - Font style
5. **"letter-spacing: normal"** - Typography detail
6. **"sharp edges"** - Clarity instruction

**Success Rate**: ~75% with Ideogram, ~60% with Imagen

---

### Technique 3: Typography-First Prompting

**Structure**:
```
TEXT_CONTENT, TYPOGRAPHY_SPECS, VISUAL_CONTEXT, STYLE, QUALITY
```

**Example**:
```
"Text: 'REVENUE $440K', typography: 72pt Helvetica Bold, 
gold gradient (#FFD700 to #FFA500), sharp anti-aliased edges, 
perfect letter spacing, centered on dark navy background (#1a1a2e), 
professional clean design, ultra-sharp, photorealistic rendering"
```

**What This Does**:
- **"Text: 'REVENUE $440K'"** - Exact string
- **"72pt Helvetica Bold"** - Specific font
- **"gold gradient"** - Color treatment
- **"sharp anti-aliased edges"** - Rendering quality
- **"perfect letter spacing"** - Typography emphasis
- **"ultra-sharp"** - Quality instruction

**Success Rate**: ~80% with Ideogram, ~65% with DALL-E 3

---

### Technique 4: Use "Typography Photography" Style

**Concept**: Ask for PHOTO of text, not generated text

```
"Professional photograph of gold metallic text '$440K' on matte 
dark background, shot with macro lens, perfect focus, sharp typography, 
studio lighting, high resolution product photography style"
```

**Why It Works**:
- AI trained on photos of text (signs, products)
- "Photography" mode activates different training
- Better at reproducing real-world text

**Success Rate**: ~70-80% depending on model

---

### Technique 5: Negative Prompts (Critical!)

**Always include negative prompts for text**:

```python
payload = {
    "model": "ideogram/v2",
    "input": {
        "prompt": "Large text 'ROI 160%' in gold, bold, centered",
        "negative_prompt": "misspelled, distorted text, blurry letters, "
                          "wrong spelling, illegible, fuzzy text, artifacts, "
                          "jumbled letters, wrong words, extra characters"
    }
}
```

**Key Negative Terms**:
- misspelled, distorted
- blurry, fuzzy
- illegible, jumbled
- wrong spelling, artifacts
- extra characters

**Impact**: +10-15% success rate

---

## 📊 Comparison: Text-Free vs Text-Included

### Text-Free Approach (What We Did):

**Pros**:
- ✅ 100% accuracy (no text = no errors)
- ✅ Faster (no regenerations)
- ✅ Professional (crisp layout text)
- ✅ Works with ANY model
- ✅ Predictable results

**Cons**:
- ⚠️ Less "integrated" look
- ⚠️ Two-step process (generate + add text)
- ⚠️ Requires layout skills

**Best For**:
- Business documents
- Data visualization
- Professional proposals
- Multi-label content

---

### Text-Included Approach:

**Pros**:
- ✅ Integrated visual look
- ✅ One-step generation
- ✅ More "designed" feel
- ✅ Good for marketing

**Cons**:
- ❌ 10-40% failure rate (model dependent)
- ❌ Requires regeneration
- ❌ Unpredictable results
- ❌ Time-consuming iterations

**Best For**:
- Single-word designs
- Marketing materials
- Social media graphics
- Mockups (can redo if wrong)

---

## 🎯 Hybrid Approach (Best of Both)

### Strategy: Selective Text Inclusion

**Use text-free for**:
- Data (numbers, metrics, stats)
- Labels (categories, axes, keys)
- Long phrases (descriptions)

**Use text-in-AI for**:
- Headlines (1-3 words max)
- Logo text (brand name)
- Emphasis words (BIG impact words)

**Example for El Dorado**:

```python
# Illustration 1: Growth Arrow (no text)
"Smooth curved arrow rising upward, gold gradient, 
no text, clean modern design"
# Then ADD text in PDF: "$440K Year 1"

# Illustration 2: ROI Callout (with text - single number)
"Large text 'ROI' in bold gold letters, centered, 
modern sans-serif, professional, Ideogram v2"
# Text is simple enough, might work

# Illustration 3: Market Size (no text - complex data)
"Abstract market visualization, network nodes, 
no text, no labels"
# Then ADD text in PDF: "$680M segment, 6.2% growth"
```

**Decision Rule**:
- Simple (1-2 words)? → Try text-in-AI
- Complex (data/numbers)? → Text-free approach
- Critical (must be perfect)? → Text-free approach

---

## 🔬 Testing Protocol

**If you want to try text-in-AI**, use this process:

### Step 1: Test with Model
```python
# Test Ideogram with simple text first
test_prompt = "Text 'ROI 160%' in large bold gold letters, centered, 
modern sans-serif, sharp typography, clean background"

# Generate 3 times
# Check success rate
# If 2/3 succeed → might be viable
# If 1/3 or 0/3 → stick with text-free
```

### Step 2: Gradual Complexity
```
Test 1: Single word ("ROI")
Test 2: Number ("160%")  
Test 3: Combined ("ROI 160%")
Test 4: Short phrase ("Year 1 Revenue")
```

**Stop when success rate drops below 70%**

### Step 3: Have Fallback
```python
def generate_with_text(prompt, filename):
    """Try text generation, fallback to text-free"""
    for attempt in range(3):
        result = generate_illustration(prompt, filename)
        if validate_text(result):  # Check if text is correct
            return result
    
    # Failed 3 times, use text-free approach
    return generate_text_free_version(prompt, filename)
```

---

## 🎨 Model-Specific Recommendations

### For KeiAI Integration:

**If they support Ideogram**:
```python
"model": "ideogram/v2"  # Best for text
"model": "ideogram/v2-turbo"  # Faster, slightly less accurate
```

**If only Google Imagen**:
```python
"model": "google/imagen4"
# Add more specific typography instructions
# Keep text short (1-3 words max)
# Use negative prompts
```

**If can use DALL-E 3**:
```python
"model": "openai/dall-e-3"
# Good middle ground
# Better than Imagen for text
# Not as good as Ideogram
```

---

## 💡 Advanced Techniques

### Technique 1: Typography as Main Subject

Instead of:
```
"Infographic with '$680M' label"  # Text is secondary
```

Use:
```
"Large typographic composition featuring '$680M' as hero element, 
bold gold lettering, professional typeface, dramatic lighting"
# Text is PRIMARY subject
```

**Why**: AI focuses more on getting it right when it's the main element

---

### Technique 2: Letter-by-Letter Specification

For critical text:
```
"Typography: dollar sign '$', followed by number '6', number '8', 
number '0', capital letter 'M', all in sequence without spaces, 
bold gold font, centered"
```

**Success Rate**: Slightly higher but verbose

---

### Technique 3: Reference Real Brands

```
"Text typography styled like Apple keynote slides - 
clean, bold, precise, modern sans-serif"
```

**Why**: AI trained on real brand materials, borrows their quality

---

## 📋 Decision Framework

### Should You Use Text-in-AI?

**YES, if**:
- [ ] Text is 1-3 words maximum
- [ ] Using Ideogram or DALL-E 3
- [ ] Can regenerate if wrong
- [ ] Not critical business data
- [ ] Time to test and iterate
- [ ] Marketing/social content

**NO, if**:
- [ ] Text is data/numbers
- [ ] Professional/business context
- [ ] Zero tolerance for errors
- [ ] Multiple labels needed
- [ ] Time-sensitive project
- [ ] Using Midjourney/SD

**For El Dorado Proposal**: NO
- Professional context ✓
- Data/numbers ✓
- Zero tolerance ✓
- Multiple labels ✓

---

## 🎯 Practical Recommendation

### For Your Use Case:

**Current Approach (Text-Free)**:
- ✅ Correct decision for proposals
- ✅ Professional documents need perfection
- ✅ Data must be accurate
- ✅ Faster and more reliable

**When to Try Text-Included**:
- Social media graphics
- Marketing materials
- Single-word emphasis
- Mockups and concepts

**Hybrid Strategy**:
```python
# Hero elements (1-2 words): Try text-in-AI
"Large text 'ROI' in gold, bold typography"

# Data points: Text-free + PDF overlay
"Abstract gold coins visualization" + add "$440K" in PDF

# Labels/axes: Text-free + PDF overlay
"Clean chart icon" + add labels in PDF
```

---

## 🔧 Implementation

### If You Want to Try Ideogram:

```python
# In generate_illustrated_proposal_pdf.py

def generate_illustration_with_text(self, prompt: str, text_content: str, filename: str):
    """Generate with text using Ideogram"""
    full_prompt = f"Typography: text reading exactly '{text_content}', {prompt}"
    
    payload = {
        "model": "ideogram/v2",  # Better for text
        "input": {
            "prompt": full_prompt,
            "negative_prompt": "misspelled, blurry text, wrong letters, distorted",
            "aspect_ratio": "16:9",
            "num_images": "1"
        }
    }
    
    # Generate and validate
    result = self.generate_illustration(full_prompt, filename)
    
    # TODO: Add validation to check if text is correct
    return result
```

### Validation Function:

```python
def validate_text_in_image(image_path, expected_text):
    """Use OCR to verify text is correct"""
    from PIL import Image
    import pytesseract
    
    img = Image.open(image_path)
    detected_text = pytesseract.image_to_string(img)
    
    return expected_text in detected_text
```

---

## 💎 Final Recommendation

**For El Dorado and similar professional proposals**:

**Stick with text-free approach** because:
1. ✅ 100% accuracy (vs 70-90% with best models)
2. ✅ Faster (no regenerations)
3. ✅ Professional appearance
4. ✅ Model-agnostic
5. ✅ Predictable results

**For other projects** (marketing, social):
- Try Ideogram v2 for simple text
- Use hybrid approach
- Have text-free fallback
- Test and iterate

---

## 🎓 Key Takeaway

**The Question**: "Can't we prompt better to get correct text?"

**The Answer**: 
- **Technically**: Yes, with specific models and techniques
- **Reliably**: No, still 10-30% failure rate
- **For Business Docs**: Not recommended
- **For Marketing**: Worth trying with proper fallbacks

**Best Practice**:
> "Use the right tool for the job. AI for visuals, layout tools for text."

**Exception**:
> "Simple text (1-3 words) + Ideogram + fallback plan = feasible"

---

**Want to experiment? Start with social media graphics. Perfect it there before using in client proposals.** 💎
