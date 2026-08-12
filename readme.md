# 一个关于webssh工具的尝试

## 主要流程
通过浏览器终端敲命令，然后前端用websocket把命令发送到后端，后端通过ssh协议发送到远程服务器，远程服务器再返回结果，后端再通过websocket返回前端，前端再把内容渲染到服务器终端。

## 需要注意的点
交互式 shell 的数据不走chan，走的是 data\_received 回调。

## todo:
- [x] 完善前端界面
- [x] 完善登录页
- [x] 美化登录界面
- [x] 密钥认证
- [x] 完善文件层级

## 问题总结
环节	发生了什么
表象	resize JSON 被当成按键写进了 shell，bash 回显到终端
直接原因	await 用在了一个非协程方法上 → 抛 TypeError
帮凶	except (json.JSONDecodeError, TypeError) 把这个真实错误静默吞掉，程序若无其事地继续执行，把 JSON 写进了 shell
两个教训：

except 只捕获明确预期的异常。把 TypeError 放进去本意是兼容消息类型，结果它成了"吞错器"，把一个真正的代码 bug 伪装成了正常流程。正确的写法是只捕 json.JSONDecodeError——其他任何错误都应该让它响亮地炸出来，而不是变成垃圾输入。
遇到"日志显示一切正常但行为不对"，先怀疑异常被吞了。排查时把 except 里的异常打印出来（except X as e: print(e)），或者干脆暂时注释掉 except。