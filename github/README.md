# BIGSCity Laboratory Website (GitHub Pages Version 1 - Original Style Clone)

北京航空航天大学智慧城市课题组（BIGSCity）官方主页 - GitHub Pages 纯静态原版复刻版（版本 1）

---

## 一、版本特性与架构设计
1. **100% 忠实复刻原版视觉风格**：
   - 保留原 Jimdo 经典的学术布局、字体层次、侧边栏排版及配色方案；
   - 彻底解除所有对 Jimdo 外部服务器、跟踪脚本（Statcounter / ClustrMaps）及 Cookie 弹窗的依赖，所有样式（`layout.css`, `main.css`, `font.css` 等）与脚本全部本地化。
2. **优雅的导航过滤与历史归档开关**：
   - **默认主导航**：保持简洁清爽（Home, Jingyuan Wang, Publications, Students & Alumni, LibCity, Visualizations, Seminars, Readings, Contact Us）；
   - **单篇论文与特刊子页**：不在侧栏主目录展开 80+ 篇子链接，而是通过各板块的汇总页面点击进入，页面完备可正常访问；
   - **归档历史栏目开关**：侧栏底部配备「🗂️ 归档/历史栏目」交互开关，默认折叠前期迭代的旧栏目（Interpretable ML、Application Fields、Maps、TCP-FIT Family 等），勾选即可实时展开，并通过 `localStorage` 跨页面自动记忆！
3. **针对 GitHub Pages 的专属优化**：
   - 根目录下包含 `.nojekyll` 文件，避免 GitHub Pages 过滤特殊文件；
   - 包含 `CNAME` 文件，预置域名绑定；
   - 全静态设计，支持 GitHub Pages、Cloudflare Pages、Vercel 或实验室自租 Linux 服务器（Nginx / Apache）零配置部署。

---

## 二、部署到 GitHub Pages 快速指南（3 步上线）

### 第 1 步：上传代码到 GitHub 仓库
1. 在 GitHub 上新建一个仓库（例如命名为 `bigscity-site`，建议设为 Public）；
2. 将本工程目录下的全部文件上传或 push 到仓库的 `main`（或 `master`）分支根目录。

### 第 2 步：开启 GitHub Pages 服务
1. 进入 GitHub 仓库页面，点击顶部的 **Settings**（设置）；
2. 在左侧菜单找到 **Pages**；
3. 在 **Build and deployment** 下：
   - **Source** 选择 `Deploy from a branch`；
   - **Branch** 选择 `main` 分支，路径选择 `/ (root)`；
   - 点击 **Save**（保存）；
4. 等待 1~2 分钟，GitHub Pages 将自动部署成功并生成访问链接（如 `https://<your-username>.github.io/bigscity-site/`）。

### 第 3 步：绑定原有独立域名（可选）
如果您希望继续使用实验室的原有域名或新申请的高校域名：
1. 在 **Settings -> Pages** 的 **Custom domain** 框中，输入您的域名（如 `smartcity-buaa.jimdoweb.com` 或 `lab.buaa.edu.cn`）；
2. 点击 **Save**；
3. 根据提示前往您的域名解析控制台（如 DNS 提供商），添加一条 CNAME 解析记录，指向 `<your-username>.github.io`；
4. 勾选 **Enforce HTTPS** 即可自动开启免费 SSL 安全证书。

---

## 三、目录结构概览
```text
├── index.html                                   # 网站首页
├── .nojekyll                                    # GitHub Pages 必需标记
├── CNAME                                        # 自定义域名配置
├── README.md                                    # 部署与维护指引
│
├── assets/                                      # 完全本地化的样式与交互脚本
│   ├── css/                                     # 原版 CSS (layout, main, font, web_oldtemplate)
│   └── js/                                      # 归档栏目切换开关 (nav_toggle.js, config.js)
│
├── contact-us/index.html                        # 联系方式
├── jingyuan-wang/index.html                     # 导师个人主页
├── libcity/index.html                           # LibCity 算法库
├── publications/index.html                      # 论文成果总库（正文包含各篇链接）
├── students-alumni/index.html                   # 学生与校友（正文包含各篇链接）
├── students-alumni/<slug>/index.html            # 82 篇论文成果单页详情
├── seminars/index.html                          # 学术研讨会
├── seminars/files/index.html                    # 研讨会 41 份 PPTX/PDF 幻灯片库
├── readings/index.html                          # 文献研读
├── readings/special-issues/index.html           # 专刊合集
├── readings/special-issues/si1/ ~ si8/          # 8 期特刊单页
├── visualizations/index.html                    # 时空可视化
│
├── application-fields/index.html                # 【归档/历史栏目】应用领域
├── interpretable-ml/index.html                  # 【归档/历史栏目】可解释机器学习
├── maps/index.html                              # 【归档/历史栏目】地图表征
├── knowledge-fusion/index.html                  # 【归档/历史栏目】知识融合
├── st-pattern-mining/index.html                 # 【归档/历史栏目】时空模式挖掘
├── tcp-fit-family/index.html                    # 【归档/历史栏目】TCP 拥塞控制
├── veccity/index.html                           # 【归档/历史栏目】VecCity
└── special-issues/urban-computing/index.html    # 【归档/历史栏目】城市计算特刊
```
