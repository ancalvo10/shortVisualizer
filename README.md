# ShortsReel

Paste a YouTube channel link and get a playlist with all of that channel's Shorts. You can open the playlist on YouTube, and the Shorts also play right in the page, each one repeated as many times as you choose.

ShortsReel is a single static page (`dist/index.html`). It has no build step, no backend and no dependencies to install.

## Run it locally

Serve the `dist` folder over HTTP with any static server, for example Python's built-in one:

```bash
python -m http.server 8765 --directory dist
```

Then open <http://localhost:8765>.

Opening `index.html` straight from disk (`file://`) may not work, because YouTube's embedded player expects a real web origin.

## Deploy

Any static host works: upload the contents of `dist/`. `disco.json` already describes a static service that publishes `dist`.

## What you can paste

| Input | Example |
|---|---|
| A channel's Shorts page | `https://www.youtube.com/@name/shorts` |
| Any channel link, or just the handle | `https://www.youtube.com/@name`, `@name` |
| A channel ID or `/channel/` link | `UC…`, `https://www.youtube.com/channel/UC…` |
| A YouTube playlist link | `https://www.youtube.com/playlist?list=…` |
| A `watch_videos` link | `https://www.youtube.com/watch_videos?video_ids=…` |
| A single video or Short | `https://youtu.be/…`, `https://www.youtube.com/shorts/…` |
| Comma-separated video IDs | `k3H3WL2jWpU,eUOFS3jhWOY` |

Keyboard: <kbd>←</kbd> and <kbd>→</kbd> switch to the previous or next short.

## How it works

1. **Find the channel ID.** If the link already contains it (`UC…`), it is used directly. For an `@handle`, the page reads the channel's Shorts page once through a public CORS proxy, because browsers cannot read youtube.com directly. The ID is then cached in `localStorage`, so the proxy isn't needed again for that channel.
2. **Build the playlist.** Every channel has an auto-generated playlist that holds only its Shorts. Its ID is the channel ID with `UC` replaced by `UUSH`. This link holds every Short, and YouTube keeps it up to date as the channel posts new ones.
3. **Read the video list.** A hidden YouTube embedded player cues that playlist and reports its video IDs. No proxy is involved in this step.
4. **Play.** The visible player plays the Shorts in order, repeating each one the chosen number of times.

The result card also offers `watch_videos` links in groups of 50. These links keep the exact current order, but they are a fixed snapshot.

## Limits

- **200 Shorts in the page player.** YouTube's embedded player only exposes the first 200 videos of a playlist. On bigger channels the page plays the latest 200, but the YouTube playlist link still contains all of them.
- **50 videos per `watch_videos` link.** YouTube silently drops every ID after the 50th, so longer lists are split into several links.
- **Proxies.** The `@handle` lookup depends on public CORS proxies (`r.jina.ai` first, then `allorigins` and `codetabs`), which can go down or rate-limit. If the lookup fails, paste the channel ID instead. On YouTube, open the channel's About panel, choose Share channel, then Copy channel ID.
- Private, deleted or embed-restricted videos are skipped automatically.

## Privacy

Nothing is stored on a server. The only data kept is the channel ID cache in your browser's `localStorage` (key `shortsreel.channels`). When an `@handle` has to be looked up, its channel page URL is sent to the proxy service.

## Project structure

```
dist/
  index.html   the whole app: markup, styles and script
  ornus2.py    original yt-dlp script, kept for reference (no longer needed)
disco.json     static hosting config (publishes dist/)
LICENSE        MIT
```

`ornus2.py` prints a single `watch_videos` link. Because of YouTube's 50-video limit, that link drops every Short past the 50th, so the web page replaces it.

## License

MIT. See [LICENSE](LICENSE).
