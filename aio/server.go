package main

import (
	"fmt"
	"time"
	"strconv"
	"github.com/gin-gonic/gin"
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
)
const DB = "root:750750750@tcp(localhost:3306)/test?charset=utf8&parseTime=True&loc=Local"
type Task struct {
	task_id int
	task_name string
	status sql.NullString
	start_time string
	end_time sql.NullString
}

func createTask(c *gin.Context) {
	db, _ := sql.Open("mysql", DB)
	defer db.Close()
	taskName := c.DefaultPostForm("task_name", "default")
	res, _ := db.Exec("insert into task(task_name, start_time) values(? ,?)", taskName, time.Now())
	task_id, _ := res.LastInsertId()
	go func (task_id int64) {
		db, _ := sql.Open("mysql", DB)
		defer db.Close()
		fmt.Println("Work.....")
		time.Sleep(1e8)
		_, err := db.Exec("update task set status='50%' where id=?", task_id)
		if err != nil {
			fmt.Println("Error......", err)
		}
		time.Sleep(5e8)
		fmt.Println("Work.....")
		db.Exec("update task set status='100%' where id=?", task_id)
		db.Exec("update task set end_time=? where id=?", time.Now(), task_id)
	}(task_id)
	c.JSON(200, gin.H{
		"status": "ok",
		"task_id": task_id,
	})
}
func fetchTask(c *gin.Context) {
	taskId := c.Query("task_id")
	if taskId == "" {
		res := queryTask("")
		var msg []map[string] string
		for _, task := range res {
			task_id := strconv.Itoa(task.task_id)
			msg = append(msg, map[string]string {
				"task_id": task_id,
				"task_name": task.task_name,
				"status": task.status.String,
				"start_time": task.start_time,
				"end_time": task.end_time.String,
			})
		}
		c.JSON(200, gin.H{
			"status": "all",
			"message": msg,
		})
	} else {
		res := queryTask(taskId)
		fmt.Println(res)
		var msg []map[string] string
		for _, task := range res {
			task_id := strconv.Itoa(task.task_id)
			msg = append(msg, map[string]string {
				"task_id": task_id,
				"task_name": task.task_name,
				"status": task.status.String,
				"start_time": task.start_time,
				"end_time": task.end_time.String,
			})
		}
		c.JSON(200, gin.H{
			"task_id": taskId,
			"message": msg,
		})
	}
}

func queryTask(taskId string) []Task {
	db, _ := sql.Open("mysql", DB)
	defer db.Close()
	var tasks []Task
	sql := "select * from task"
	if taskId != "" {
		suffix := " where id=" + taskId
		sql += suffix
	}
	rows, _ := db.Query(sql)
	defer rows.Close()
	for rows.Next() {
		var task Task
		rows.Scan(&task.task_id, &task.task_name, &task.status, &task.start_time, &task.end_time)
		tasks = append(tasks, task)
	}
	return tasks 

}
func main() {
	r := gin.Default()
	r.GET("/task", fetchTask)
	r.POST("/task", createTask)
	r.Run(":8080")
}