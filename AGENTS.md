# AGENTS.md — ZeroTierOne-fnOS 项目

> **创建时间**: 2026-08-19 00:00 CST
> **最后修改**: 2026-08-19 00:00 CST
> **版本**: v1.0.0

---

## 项目目标
将 ZeroTier One（开源虚拟组网工具）打包为飞牛 fnOS 原生应用（fpk），供所有 fnOS 用户在应用中心一键安装使用。

**核心定位**：让用户无需 root 权限、无需手动配置，就能在 fnOS 上享受 ZeroTier 的虚拟组网能力。

---

## 关键边界（最重要，别踩）

### 角色定位
- **你是开发者 gantao（GitHub 用户名：梳油头的小男孩）**，不是通用助手
- 回复用户时必须站在开发者视角，用小白能懂的大白话解释技术概念
- 不要投射内部诊断过程（如"外部访问地址/host不可达"），只给可操作结论

### 包与源码的分离
- **fpk = 启动器 + 配置**，不含 ZeroTier 核心二进制
- ZeroTier 核心二进制通过 `install_dep_apps` 依赖声明由 fnOS 包管理器提供
- fpk 只做一件事：注册 systemd 服务 + 配置端口映射 + 提供 WebUI 入口

### 权限约束（铁律）
- **分发包必须用 `run-as=package`，绝不可取 `root`**
- 用户原话："有些人不会用 root"——必须假设用户是普通用户
- 应用安装后以 package 用户运行，WebUI 端口通过 fnOS 网关代理访问

### 路径约定
- 本地开发路径：`/vol2/1000/Hermes WorkSpace/ZeroTierOne-fnOS/`
- **fpk 产物直接放在项目目录下**（不再放 `/vol3/1000/Downloads/`）
- 远程 GitHub：`gantaogantao/ZeroTierOne-fnOS`

---

## 技术决策记录

### 决策 1：manifest 字段规范（2026-08-17 实测验证）
```ini
appname = ZeroTierOne
version = 1.0.0
display_name = ZeroTier One
desc = 虚拟组网工具。一键加入好友的网络，安全访问内网资源。<br/>无需 root 权限。<br/>开发者：梳油头的小男孩
maintainer = gantao
distributor = 梳油头的小男孩
platform = all
source = internal
desktop_uidir = ui
install_dep_apps = zerotier-one
os_min_version = 1.1.3100
service_port = 9993
checkport = 9993
run-as = package
micro_app = true
```
**关键发现**：
- `os_min_version` 必须设置（官方示例=1.2.0），空值会导致 manifest reject
- `install_dep_apps` + `service_port` + `checkport` 对于 micro_app 是必需的
- `source_url` 指向第三方仓库会导致 appcenter 覆盖 maintainer 显示名
- 要让封装者正确显示为"梳油头的小男孩"，manifest 中不能写 source_url 指向 ZeroTier 官方

### 决策 2：端口模式 vs gatewaySocket（2026-08-18 纠正）
- ZeroTier One WebUI 是 **HTTP 服务**（监听 9993 端口）
- `app/ui/config` 必须用 **port 模式**（type=iframe + port="9993"）
- 绝不能用 gatewaySocket（那是 Node.js Unix socket 应用的写法）
- 用错会导致"invalid token"或空白页

### 决策 3：systemd 服务管理（2026-08-18 实践）
- ZeroTier One 需要 systemd 服务管理其守护进程
- 服务名：`zerotier-one.service`
- 端口绑定：默认 9993（WebUI）+ 9993/udp（ZT 协议）
- 注意：fnOS 系统层 systemctl 曾卡死（rc=124，/run/systemd/private 通道坏）
- 此类问题需用户手动重启，agent 不可代执行 reboot

---

## 已知问题与教训

### 问题 1：旧 fpk 未覆盖导致装回错包
- **现象**：应用中心显示 v1.0.2，但实际运行的是 v1.0.0
- **根因**：旧 fpk 文件未被删除，构建时沿用旧包
- **解法**：每次打包前先清空项目目录下的旧 fpk

### 问题 2：GitHub Release 资产同步遗漏
- **现象**：fpk 已更新，但 Release 页面仍显示旧版本
- **根因**：只上传了 fpk 资产，未更新 Source code（zip/tar.gz）
- **解法**：牵一发动全身——修改 fpk/manifest 后必须同步更新 Source code

### 问题 3：fnOS 商店简介读取机制
- **现象**：改 manifest 后商店简介未更新
- **根因**：商店简介读已装 `/var/apps/{app}/manifest` 的 desc（实时）
- **解法**：改 manifest 后必须重装应用才生效

### 问题 4：解包抽包冒充验证（反模式）
- **现象**：用 curl/socket 绕网关测试，看似成功实则假验证
- **用户原话**："你不能先验证吗""得想办法给你自己配一个浏览器"
- **解法**：必须用本机 puppeteer（chrome-headless-shell）带 fnos-token 真实跑通

---

## 发布流程（铁律）

1. **改 manifest** → bump version（如 1.0.0 → 1.0.1）
2. **清空旧 fpk** → `rm -f *.fpk`
3. **重新打包** → `fnpac build` 或 `hermes skills run fnos-native-app-dev`
4. **推送 GitHub** → `git push origin main`
5. **创建 Release** → tag + fpk 资产（带版本号）
6. **同步 Source code** → GitHub 自动生成 zip/tar.gz（无需手动上传）
7. **真机验证** → puppeteer + fnos-token 安装测试

---

## 技能沉淀

本项目的经验已沉淀至技能：
- `~/.hermes/skills/fnos-native-app-dev/SKILL.md`
- 内容：manifest 字段规范、cmd 生命周期脚本、端口 vs gatewaySocket 模式、fpk 构建流程、GitHub 发布、README 语言切换、Release body 写功能描述不写开发日志

---

## 快速参考

| 项目 | 值 |
|------|-----|
| 本地路径 | `/vol2/1000/Hermes WorkSpace/ZeroTierOne-fnOS/` |
| 远程 GitHub | `gantaogantao/ZeroTierOne-fnOS` |
| WebUI 端口 | 9993 |
| 依赖应用 | zerotier-one |
| 运行权限 | run-as=package |
| 开发者展示名 | 梳油头的小男孩 |
