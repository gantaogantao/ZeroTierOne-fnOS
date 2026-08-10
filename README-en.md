# ZeroTier One for fnOS

[中文说明](README.md) | English

![Version](https://img.shields.io/badge/version-1.3.7-blue)
![License](https://img.shields.io/badge/license-MIT%20%2F%20BSL--1.1-green)
![Platform](https://img.shields.io/badge/platform-fnOS%20%2F%20x86__64-orange)
![BasedOn](https://img.shields.io/badge/based%20on-ZeroTier%20One-success)

A native ZeroTier One client for feiniu fnOS, with a visual web management UI for remote LAN access.

## 🛠 Features

* **Native Integration**: Compiled natively for fnOS environment, ensuring stability under high-concurrency data transfer.
* **Visual Web Management Panel**:
  * **Status Indicator**: CSS animated "breathing light" shows real-time service status.
  * **Network Management**: Quickly join any ZeroTier network with 16-digit Network ID.
  * **IP Tracking**: Real-time API polling displays VPN IP addresses across multiple network segments.
* **High Performance Hole Punching**: P2P direct connection technology minimizes latency for cross-network access.

## ⚙️ Technical Details

* Default Listen Port: `9994` (TCP)
* Storage Path: Configuration persisted at `/var/lib/zerotier-one`
* UI Framework: Built with Tailwind CSS and HTML5 Canvas animation engine

## 📝 Developer's Note

This application improves the networking experience for fnOS users, bringing the hidden background binary process to life with a vibrant UI.

## ⚖️ License

Follows ZeroTier's open-source license and MIT license.

## 📸 Screenshots

### Home Page
![Home](screenshots/screenshot1.png)

### Connected Celebration Effect
![Connected](screenshots/screenshot2.png)

### Connected Status with IP Display
![Connected with IP](screenshots/screenshot3.png)

## 🔧 Installation

Manual install in fnOS App Market:

1. Download the latest `zerotierone.fpk` from Releases
2. In fnOS → App Management → Manual Install, select this file
3. Wait for installation to complete, you'll find ZeroTier One in your app list
4. Click to open the web management UI

## 📋 Compatibility

* ✅ fnOS >= v0.x (compatible with current feiNiu NAS system)
* ✅ Supports x86_64 architecture

## 📝 Changelog

### v1.3.7
* **App icon redesigned**: rounded-rectangle icon matching fnOS design spec, with a new 64px entry icon.
* **Web UI visual polish**: added a glowing background effect.
* **Web self-healing (from v1.3.6)**: if the management UI process exits unexpectedly, it auto-restarts every 30s without affecting VPN networking.

### v1.3.6
* **Fixed Web UI occasionally failing to open**: the Web subprocess (port 9994) could silently exit in some environments, while the original health check only watched the VPN core (9993), so the App Center showed "running" but the management page was actually unreachable.
  * Added a **Web self-healing watchdog**: a lightweight loop runs after app start, checking 9994 every 30s and auto-restarting the Web subprocess if it's not listening — **without affecting VPN networking (9993)**.
  * On app stop, the watchdog and Web process are cleaned up together, leaving no residue.
  * If you previously hit "App Center shows running but management page won't open / clicking open does nothing", upgrading to this version self-heals it — no more manual stop→start.
