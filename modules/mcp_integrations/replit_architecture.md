# Replit App Architecture (Media Studio)

**Overview**: A full-stack React/Express app integrated with n8n for media generation (Avatars & Images).

## 🗄️ Database Schema (Drizzle/Postgres)

### Tables
1. **users**: `id`, `username`, `password`
2. **finished_videos**:
   - `id` (serial)
   - `video_url` (text)
3. **finished_images**:
   - `id` (serial)
   - `image_url` (text)
   - `prompt` (text)
   - `service_type` (text)

---

## 🔌 API Routes (Express)

### Uploads & Files
- `GET /objects/*`: Download files
- `POST /api/objects/upload`: Get presigned URL
- `POST /api/objects/upload-image`: Upload + HEIC Conversion

### n8n Integrations
- **Avatar Studio**: `POST /api/send-to-webhook`
  - Body: `{ image_data, video_data, prompt }`
  - Target: **n8n Webhook A**

- **Image Assistant**: `POST /api/image-assistant/generate`
  - Body: `{ service_type, prompt, aspect_ratio, resolution, output_format, image_input }`
  - Target: **n8n Webhook B**

### Callbacks (n8n -> Replit)
- `POST /api/finished-videos`: Store completed video result
- `POST /api/finished-images`: Store completed image result

---

## ⚡ n8n Configuration

**Webhook URLs (Production)**:
- **Avatar Studio**: `https://innovlead.app.n8n.cloud/webhook/14fb3e23-023f-4706-a13a-1d28bd31cbe9`
- **Image Assistant**: `https://innovlead.app.n8n.cloud/webhook/d2de64ab-ce17-4cfc-a53a-c56b0c949b21`

---

## 🎨 Frontend (React)

**Routes**:
- `/` -> Dashboard
- `/avatar-studio` -> Home
- `/videos` -> Videos Gallery
- `/image-assistant` -> Image Generator

**Theme**:
- **Primary**: Blue/Cyan gradients (`#0066b3` -> `#06b6d4`)
- **Background**: Dark Navy (`#0a1628`)

---

## 🚀 Antigravity Integration Strategy

**To Generate Media:**
Do **NOT** call Replit directly. Call the **n8n Webhook** directly.

**Example (Image Gen):**
```python
requests.post(
    "https://innovlead.app.n8n.cloud/webhook/d2de64ab-ce17-4cfc-a53a-c56b0c949b21",
    json={
        "service_type": "text-to-image",
        "prompt": "Cyberpunk city",
        "aspect_ratio": "16:9"
    }
)
```
The n8n workflow will handle generation and post the result back to Replit's `/api/finished-images`.
