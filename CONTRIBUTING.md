# 贡献指南 / Contributing

感谢你对 **ZeroTier One for fnOS** 的关注！

## 项目定位 / Scope

本仓库是 **ZeroTier One 在飞牛 fnOS 上的适配层**，包含：

- `cmd/main`：fnOS 原生应用生命周期脚本（启动 / 停止 / 状态 / 自检看门狗）
- `app/server`：可视化 Web 管理界面
- 打包配置（`manifest`、`config/`、`wizard/`）与文档

**底层网络核心（ZeroTier One 守护进程与协议）版权归属上游 ZeroTier, LLC**，
本项目仅做 fnOS 平台适配与界面封装，不修改网络核心本身。
相关讨论请前往上游：https://github.com/zerotier/ZeroTierOne

## 如何贡献 / How to contribute

1. Fork 本仓库并创建分支（`git checkout -b fix/xxx`）
2. 提交改动（`git commit -m "fix: ..."`）
3. 推送并开 Pull Request，描述清楚改动目的

## 开发环境 / Dev notes

- 打包工具：`fnpack`（飞牛官方）
- 构建：`fnpack build` → 产物 `*.fpk`（通过 GitHub Releases 分发，**不进仓库**，见 `.gitignore`）
- 本地测试：在 fnOS 应用管理 → 手动安装生成的 fpk

## 许可证 / License

- fnOS 适配层：MIT（见 [LICENSE](LICENSE)）
- 底层网络核心：ZeroTier BSL-1.1（见 [LICENSE-ZeroTier](LICENSE-ZeroTier)）
