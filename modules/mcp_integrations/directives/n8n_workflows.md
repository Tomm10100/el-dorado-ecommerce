# SOP: Using n8n Cloud (Action)

**Goal**: Orchestrate complex workflows and automations.

## Capabilities
- **Trigger**: Run existing workflows
- **Create**: Build new workflows programmatically
- **Monitor**: Check for failed executions

## Standard Patterns

### 1. Triggering Automation
Dont build complex logic in Python if n8n can do it.
- **Bad**: Python script sends email via SMTP
- **Good**: Python script triggers `send-email` workflow in n8n

### 2. Creating Workflows
If a requested automation doesn't exist:
1. Research best practice
2. Generate JSON definition for n8n workflow
3. Use `create_workflow()` to deploy it
4. Test run

## Naming Convention
- `[Service] - [Action] - [Version]`
- Example: `Client - Onboard - v2`
