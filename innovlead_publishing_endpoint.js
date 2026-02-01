// InnovLead - Social Media Publishing Endpoint
// Add this to your server.js in Replit

const axios = require('axios');
const fs = require('fs').promises;

// Environment variables
const N8N_SOCIAL_WEBHOOK = process.env.N8N_SOCIAL_WEBHOOK || '';

// Social media publishing endpoint
app.post('/api/social-publish', async (req, res) => {
    try {
        const { title, content, image_url, platforms, tags } = req.body;

        // Validate input
        if (!title || !content) {
            return res.status(400).json({
                success: false,
                error: 'Title and content are required'
            });
        }

        console.log(`📱 Publishing: ${title}`);
        console.log(`📝 Content: ${content.substring(0, 50)}...`);
        console.log(`📸 Image: ${image_url || 'No image'}`);
        console.log(`📢 Platforms: ${platforms?.join(', ') || 'instagram, tiktok'}`);

        // Option 1: Forward to n8n if webhook configured
        if (N8N_SOCIAL_WEBHOOK) {
            try {
                const response = await axios.post(N8N_SOCIAL_WEBHOOK, {
                    title,
                    content,
                    image_url,
                    platforms: platforms || ['instagram', 'tiktok'],
                    tags: tags || [],
                    timestamp: new Date().toISOString()
                }, {
                    timeout: 10000
                });

                console.log('✅ Forwarded to n8n successfully');

                return res.json({
                    success: true,
                    id: Date.now().toString(),
                    message: 'Content queued for publishing via n8n',
                    platforms: platforms || ['instagram', 'tiktok']
                });
            } catch (n8nError) {
                console.error('⚠️ n8n webhook failed:', n8nError.message);
                // Fall through to queue-based approach
            }
        }

        // Option 2: Save to queue (fallback or default)
        console.log('💾 Saving to local queue (n8n not configured or failed)');

        const queueFile = './social_queue.json';

        let queue = [];
        try {
            const data = await fs.readFile(queueFile, 'utf8');
            queue = JSON.parse(data);
        } catch (e) {
            queue = [];
        }

        const post = {
            id: Date.now().toString(),
            title,
            content,
            image_url,
            platforms: platforms || ['instagram', 'tiktok'],
            tags: tags || [],
            status: 'pending',
            created_at: new Date().toISOString()
        };

        queue.push(post);

        await fs.writeFile(queueFile, JSON.stringify(queue, null, 2));

        console.log(`✅ Saved to queue (Total: ${queue.length} posts)`);

        return res.json({
            success: true,
            id: post.id,
            message: 'Content saved to queue',
            queue_size: queue.length,
            note: N8N_SOCIAL_WEBHOOK ? 'n8n failed, saved locally' : 'Set N8N_SOCIAL_WEBHOOK for auto-publishing'
        });

    } catch (error) {
        console.error('❌ Publishing error:', error.message);

        return res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// View queued posts
app.get('/api/social-queue', async (req, res) => {
    try {
        const data = await fs.readFile('./social_queue.json', 'utf8');
        const queue = JSON.parse(data);

        res.json({
            success: true,
            total: queue.length,
            pending: queue.filter(p => p.status === 'pending').length,
            published: queue.filter(p => p.status === 'published').length,
            queue: queue
        });
    } catch (error) {
        res.json({
            success: true,
            total: 0,
            pending: 0,
            published: 0,
            queue: []
        });
    }
});

// Mark post as published (manual workflow helper)
app.post('/api/social-queue/:id/publish', async (req, res) => {
    try {
        const { id } = req.params;
        const data = await fs.readFile('./social_queue.json', 'utf8');
        let queue = JSON.parse(data);

        const post = queue.find(p => p.id === id);
        if (post) {
            post.status = 'published';
            post.published_at = new Date().toISOString();

            await fs.writeFile('./social_queue.json', JSON.stringify(queue, null, 2));

            res.json({
                success: true,
                message: 'Post marked as published',
                post
            });
        } else {
            res.status(404).json({
                success: false,
                error: 'Post not found'
            });
        }
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});
