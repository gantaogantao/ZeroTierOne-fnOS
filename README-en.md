# ZeroTier One for fnOS

Native ZeroTier One client package customized for **fei牛 (fnOS) NAS system**, featuring high-performance network service with a modern web-based management UI.

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
