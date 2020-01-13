# asyncio 与 goroutine 实现常见异步场景比较代码



启动文件, go文件可以直接使用`go run server.go` 启动, 需要开启`mysql`服务.

使用`curl` 测试

```
curl -X POST http://localhost:8080/task -d '{"task_name": "test"}'

curl -X GET http://localhost:8080/task
curl -X GET http://localhost:8080/task?task_id=6
```
