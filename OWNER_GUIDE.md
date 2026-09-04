# SOVRAIL AI — Owner Guide

## What it is
SOVRAIL AI is Wilkerson Collective’s own front door for software-to-software calls. Your apps call SOVRAIL first instead of each app directly calling OpenAI, Anthropic, Tavus, or another provider.

## What that means in plain English
Think of SOVRAIL as a company switchboard plus purchasing manager. A WCL product asks SOVRAIL for a job. SOVRAIL checks whether the job is allowed, tries the lowest-cost approved way to do it, keeps the outside company’s secret key away from the product, records what happened, and can switch providers if one is unavailable.

## Where it lives
The permanent source-of-truth is this GitHub repository. A deployed copy should run on WCL-controlled infrastructure such as Render or another server. Future WCL products connect to that live SOVRAIL service.

## How you use it
You normally should not type API code yourself. A new WCL product gets two settings: `SOVRAIL_BASE_URL` (where the live SOVRAIL service is) and `SOVRAIL_API_KEY` (that product’s private WCL-issued key). The product sends its requests there.

## Three-system relationship
SWARMER decides whether a tool/provider/capability is trusted and permitted. SOVRAIL decides how an approved call should be routed, budgeted, cached, and executed. KAMERON preserves a trusted checkpoint so interrupted work can resume instead of starting over.

## Cost reality
SOVRAIL can avoid or reduce paid model calls by using local/self-hosted models, caching repeated results, blocking duplicate calls, and choosing cheaper approved providers. It cannot make a paid provider such as Tavus, OpenAI, Anthropic, or ElevenLabs deliver its paid service for free.

## Default rule for future WCL builds
When an app needs an external AI/API connection, first route it through SOVRAIL when technically appropriate. Keep provider keys in SOVRAIL, not scattered across each product. Prefer local/self-hosted execution where it meets quality needs, and use paid providers only when needed.
