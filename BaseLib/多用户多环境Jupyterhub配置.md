# 多用户多环境Jupyter notebook配置

最近实验室新购进了一台服务器供小组科研使用，部署多人协作使用jupyter时碰见了很多坑，现在做一个总结，也为同样需求的同行做个指南~

需求

- 服务器多用户同时使用一个端口下的jupyter notebook
- 多用户能够自己创建虚拟环境并在jupyter中使用他；用时用户可以自己对环境依赖进行定制
- OS： Ubuntu 16.04

## 多用户解决方法

- 使用Jupyterhub, 官方专门为多用户使用Jupyter提出的解决方案；

- 配置流程

  - 在**root管理员**下下载anaconda, 使用conda安装jupyerhub

  - 配置Jupyterhub

    - 生成配置文件（或自己创建）

      ``` bash
      jupyterhub --generate-config
      ```

    - 修改配置文件 （重要，默认直接启动的话只有root能够登录）

      ```python
      c.JupyterHub.ip = '*'
      c.JupyterHub.port = 端口
      c.PAMAuthenticator.encoding = '编码'
      c.LocalAuthenticator.create_system_users = True
      c.Authenticator.whitelist = {'user1', 'user1', 'user3'}
      c.Authenticator.admin_users = {'user1'}
      c.LocalAuthenticator.group_whitelist = {'group1'}
      c.JupyterHub.statsd_prefix = 'jupyterhub'
      ```

      设置用户分组，将user1, user2, user3加入到group1中（先创建好用户）

      ```bash
      adduser user1 group1
      adduser user2 group1
      adduser user3 group1
      ```

  - 在配置文件目录下启动启动jupyterhub ；直接使用Linux的用户名密码登录即可跳转到用户的主目录下；

- 注意事项

  - 必须在root管理员下启动才可以实现多用户；
  - 必须把子用户与root放在同一个用户组中子用户的jupyter才有权限读写；

## 多环境（多核）解决方案；

- 首先明确一点，python的环境管理方案有很多，如pipenv\virtualenv等；但jupyter notebook 必须使用conda的环境管理；

- 多个用户可以使用同一个anaconda3，也可以自行下载一个，不过没必要。可以直接同意使用一个用户下的conda（也可以是root下的anaconda）；

  每个用户在配置文件中做如下配置：

  ```bash
  export PATH="$PATH:\某个目录\anaconda3\bin"
  ```

  这样每个用户**在base环境下的**的python和conda路径保持了一致；可以使用which命令查看当前每个命令的路径

- 每个用户可以自己使用conda创建虚拟环境，此时创建的虚拟环境的默认保存路径是\home\USer名称\\.conda\env下面；该目录下保存了该用户创建的所有虚拟环境；每个虚拟环境下的文件包含Bin和lib等，激活环境后的python路径就变为\home\user\\.conda\env\环境名\bin\python了；

- 很简单的逻辑，python找库要首先找在其目录下的lib下；

- 此时在虚拟环境下，用户使用conda install安装的库就自然地能被python找到；**子用户创建的虚拟环境不能被其他子用户使用**，这一点在不同自用户下使用conda env list能检查出来；那什么样的环境可以多用户共享？ 答案是**conda路径拥有者创建的虚拟环境**；

- 虚拟环境与**jupyer核**的对应还需要以下几步(在虚拟环境下执行)

  ```bash
  conda isntall ipykernel
  python -m ipykernel install --user --name myenv --display-name "Python (myenv)" 
  ```

  这样jupyer notebook的界面才会有新的虚拟环境的kernel的选项；

  此时会在/home/USer/.local/kernel下生成配置文件，其实就是制定了这个kernel使用的Python路径，当然你可以自己修改；

## 几个排错方法

- 使用netstat -ntlp查看网络服务端口开启情况，检查jupyerHub是否启动
- 多使用which命令看路径，多看.bashrc配置文件中的路径；
- 友情提示：Anaconda已经不支持清华源了，因此之前如果配置了清华源现在会下载失败（这不是作死嘛。。。）所以大家要把源重新换回来，再想别的方法加速了...



