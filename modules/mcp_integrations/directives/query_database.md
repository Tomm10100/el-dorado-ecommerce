# SOP: Using Replit Database (Memory)

**Goal**: Persistently store and retrieve data for automation context.

## Principles
1. **Key-Value Only**: Don't try to store complex relational data. Use JSON blobs.
2. **Ephemeral vs Persistent**: 
   - Use `.tmp/` for file processing (images, large text)
   - Use DB for metadata, status, and logs.

## Schema Conventions
- `client:{client_name}` -> Dict of client info
- `logs:{module_name}` -> List of last 100 execution logs
- `config:{key}` -> Global configuration overrides

## When to Use
- **Client Onboarding**: Check if client exists (`client:ABC`)
- **Workflow State**: Store last run time (`last_run:daily_report`)
- **Error Tracking**: Log failures for self-healing
