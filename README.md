# Northflank 外部镜像自动刷新

[中文](./README.md) | [English](./README.en.md)

一句话说明：这个仓库会定时调用 Northflank API，重启你已经配置成 `External image` 的 service，让它重新拉取 Docker Hub 的最新镜像。

## 3 分钟部署

### 第 0 步：先准备好 Northflank API token

先去 Northflank 后台创建 token：

- https://app.northflank.com

你后面要把它填到 GitHub 的 `NF_API_TOKEN` 里。


### 第 1 步：把本目录放进你自己的 GitHub 私有仓库

不要直接用公开仓库跑这套流程。  
新建一个 GitHub 私有仓库，然后把本目录内容复制进去。

为什么建议私有仓库：

- workflow 里会写你的真实 `project ID` 和 `service ID`
- 这些信息虽然不是密码，但属于运维信息

### 第 2 步：修改 workflow 里的两个示例值

打开这个文件：

- `.github/workflows/northflank-refresh-external-image.yml`

你会看到这个示例地址：

```text
https://api.northflank.com/v1/projects/a86/services/b94/restart
```

这里的含义是：

- `a86` = `project ID` 示例
- `b94` = `service ID` 示例

你必须把它改成你自己的值。

例如：

```text
https://api.northflank.com/v1/projects/你的ProjectID/services/你的ServiceID/restart
```

### 第 3 步：在 GitHub 里添加 Secret，然后手动运行一次

进入：

- `Settings -> Secrets and variables -> Actions`

添加这个 Secret：

- `NF_API_TOKEN`

然后打开：

- `Actions`

手动运行一次 workflow，确认你的 service 能被成功重启。

## 你真正要改的只有 3 处

1. 你的 `project ID`
2. 你的 `service ID`
3. 你的 `NF_API_TOKEN`

除此之外，其他内容基本都不用动。

## 完整示例

示例地址：

```text
https://api.northflank.com/v1/projects/a86/services/b94/restart
```

字段说明：

- `a86` 是示例 `project ID`
- `b94` 是示例 `service ID`

再次强调：

- `a86 / b94` 只是示例
- 你部署时一定要换成自己的值

## 为什么这个方法能更新镜像

这套方案的前提是：

- 你的 Northflank service 已经配置成 `External image`
- 你的镜像 tag 使用的是 `latest`

然后 workflow 会调用 `restart` 接口。  
service 重启时，Northflank 会重新拉取这个外部镜像，因此就能拿到最新版本。

## 如果你的镜像不是 latest

如果你写的是固定 tag，例如：

```text
my-image:1.2.3
```

那么重启以后仍然还是这个固定版本，不会自动变成新版本。  
这套方案更适合 `latest` 这种会滚动更新的标签。

## 改定时执行时间

如果你要修改自动执行时间，改这个文件里的 `cron`：

- `.github/workflows/northflank-refresh-external-image.yml`

当前示例是：

```yaml
schedule:
  - cron: "17 4 * * 2"
```

这表示：

- 每周二
- 04:17 UTC

## 本地测试

如果你想先在本地看一下脚本会调用哪个地址，可以这样跑：

```powershell
$env:NF_API_TOKEN='your_new_token'
python .\scripts\refresh_northflank_external_image.py --dry-run
```

`--dry-run` 不会真的调用 Northflank API，只会打印目标地址。

## 目录说明

- [workflow](/E:/_BIGFA%20Free/_code/_Mywork/Northflank%20Refresh%20External%20Image/.github/workflows/northflank-refresh-external-image.yml)
- [script](/E:/_BIGFA%20Free/_code/_Mywork/Northflank%20Refresh%20External%20Image/scripts/refresh_northflank_external_image.py)

## 官方文档

- [Run an image from a container registry](https://northflank.com/docs/v1/application/run/run-an-image-from-a-container-registry)
- [Manage CI/CD](https://northflank.com/docs/v1/application/release/manage-ci-cd)
- [Restart service API](https://northflank.com/docs/v1/api/project/services/restart-service)
