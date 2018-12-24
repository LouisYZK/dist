# FluntPython 记录
实例代码在https://github.com/fluentpython/example-code
## ch3 Dict and Set
- 往字典里添加新建可能会改变已有键的顺序
> 无论何时往字典里添加新的键，Python 解释器都可能做出为字典扩容的决定。扩容导致的结果就是要新建一个更大的散列表，并把字典里已有的元素添加到新表里。这个过程中可能会发生新的散列冲突，导致新散列表中键的次序变化。要注意的是，上面提到的这些变化是否会发生以及如何发生，都依赖于字典背后的具体实现，因此你不能很自信地说自己知道背后发生了什么。如果你在迭代一个字典的所有键的过程中同时对字典进行修改，那么这个循环很有可能会跳过一些键——甚至是跳过那些字典中已经有的键。

**由此可知，不要对字典同时进行迭代和修改。如果想扫描并修改一个字典，最好分成两步来进行：首先对字典迭代，以得出需要添加的内容，把这些内容放在一个新字典里；迭代结束之后再对原有字典进行更新（Update方法）。**
- set 和dict的特点：
  - 里面的元素必须是可散列的（可哈希的）
  - dict/set很消耗内存
  - 两者可以很高效地判断元素是否存在于某个集合
  - 元素的次序取决于被添加到集合/字典里的次序
  - 往集合或字典里添加元素，可能会改变即合理已有的元素顺序

## ch4 文本和字节序列
- 概念：
  - 字符的标识，即码位，Unicode用4-6个十六进制的数字表示，用U打头
  - 字节序列，是字符的编码方式。如UTF8， 一般b打头
  - 讲字符串转换为机器识别的字节序列为编码encode(),而将字节序列转换成字符串是解码过程decode()

- python3内置了两种字节序列：bytes(不可变) 和 bytearray（可变）。 其各个元素是range(256)的整数，虽然二进制序列其实是整数序列，但是二进制序列都可以使用str对象的方法。

- 实现bytes或bytearray实例可以传入如下参数：
  - 一个str对象和一个encoding关键字
  - 一个可迭代对象，提供0-255数值
  - 一个实现了**缓冲协议**的对象（如bytes, bytearray, **memoryview**, array.array）； 使用缓冲类对象创建字节学列时，始终**复制**源对象中的字节序列，与之相反，memoryview对象允许在二进制数据结构间**共享内存**

- struct 模块可以帮助我们从bytes和memeoryview中提取结构化信息，在频繁地对二进制io操作时可以使用词模块

- 编码中的问题
  - UnicodeEncodeError错误出现在encode（'非utf_x'）时，utf_8能做到对所有字符编码，但其他的编码方式不一定。此时制定errors = 'ignore'或者'replace'替换为？.
  - UnicodeDecodeError,此错误出现在对字节序列解码时使用了不对应的编码方式。常常会出现乱码

- 处理文本文件
  - 处理文本文件的最佳方式是在业务逻辑代码环节只操作unicode, io操作字节序列。这一过程python3的read和open都已经实现了。
  - 但要注意的是，read()一个文件的时候不要依赖默认编码。open('...','r')的默认编码是系统默认编码，Linux和MacOS都是默认utf8，所以读写都不会出问题。但win默认的是cp2123,此时如果写入时制定编码utf8, 而读出时依赖系统默认编码就会出现乱码。
  - 'rb'选项读出的是字节序列。一般不是要判断字符编码方式不推荐使用此模式

- Unicode麻烦的问题在于非ASCII字符的比较和排序上（**因为unicode为某些字符提供了不同的表示**）。使用全局码和区间域的设置可以解决不同语言的比较和排序问题；PyUCA库也是专门用用来解决此问题的

- 支持字符串和字节序列的双模式API。如re 和 os模块就实现了双模式的输入。r'\d' 和rb'\d' 识别不同模式下的ASCII数字。 os中的路径也可以传入b'' 返回的也是字节序列的文件名称。

> Python3在RAM中如何表示字符串？ 在内存中，Python3使用固定数量的字节存储字符串的各个码位，以便高效访问各个字符或切片。在创建str时，解释器会检查里面的字符，然后为该字符选择最经济的内存布局（如2个或4个字节，中文大多数字两个字节够用）

## Ch5 一等函数
- 在Python中，函数被称为一等对象。因为他满足以下特点
  - 在运行时创建
  - 能赋值给变量或数据结构中的元素
  - 能作为函数参数传递
  - 能作为函数返回

- 可调用类型（callable）是可用使用（）的对象， 实现了__call__方法后对象实例也可为可调用对象，可以用内置函数callbale()判断是否为可调用对象。（生成器也是一种特殊的可调用对象）

- 函数对象有个 __defaults__ 属性，它的值是一个元组，里面保存着定位参数和关键字参数的默认值。仅限关键字参数的默认值在__kwdefaults__ 属性中。然而，参数的名称在 __code__ 属性中，它的值是一个 code 对象引用，自身也有很多属性。**inspect** 模块可以帮助我们查查看参数的对应情况

- 为函数编写的注解默认储存在内省方法__annotation__中

- 支持函数式编程的包
  - Operator模块， 如itemgetter()和attrgetter()方法
  - functools模块
    - functools.partial会冻结原函数的某个参数返回只调用部分参数的新的回调对象
    - lru_cache 函数令人印象深刻，它会做备忘（memoization），这是一种自动优化措施，它会存储耗时的函数调用结果，避免重新计算。

## Ch6 使用一等函数实现设计模式
> ：“对接口编程，而不是对实现编程”和“优先使用对象组合，而不是类继承”。
------ 《设计模式：可复用面向对象软件的基础》

模块也是一等对象，内置globals()函数可以查看当前模块所有内置对象

## ch7 函数装饰器和闭包
- 函数装饰器在导入模块时立即执行，而被装饰的函数只在明确调用时运行。大多数装饰器会在内部定义一个函数，然后将其返回。（多数装饰器都会修改函数）
;装饰器的典型行为：把被装饰的函数替换成新函数，二者接受相同的参数，而且（通常）返回被装饰的函数本该返回的值，同时还会做些额外操作。

- 函数闭包的概念要先明白Python3的变量作用域
  - Python不要求声明变量，但是嘉定在函数定义体中赋值的变量是局部变量。
  - 如果在函数中赋值时想让解释器吧某变量当做全局变量，要使用**global**声明。

- 闭包是一种函数，它会保留定义函数时存在的**自由变量**的绑定，这样调用函数时，虽然定义作用域不可用了，但是仍能使用那些绑定。**注意，只有嵌套在其他函数中的函数才可能需要处理不在全局作用域中的外部变量。**
![](https://ws1.sinaimg.cn/large/6af92b9fgy1fy7s2z1lnhj20nj0bmad0.jpg)

-  Python 3 引入了 nonlocal 声明。它的作用是把变量标记为自由变量，即使在函数中为变量赋予新值了，也会变成自由变量。如果为 nonlocal 声明的变量赋予新值，闭包中保存的绑定会更新。
```python
def make_average():
  count = 0
  total = 0
  def averager(new_value):
    nonlocal count, total
    count += 1
    total += new_value
    return total / count
  return averager
```

- 标准库中的装饰器
  - functools.lru_cache 是非常实用的装饰器，它实现了备忘（memoization）功能。这是一项优化技术，它把耗时的函数的结果保存起来，避免传入相同的参数时重复计算。LRU 三个字母是“LeastRecently Used”的缩写，表明缓存不会无限制增长，一段时间不用的缓存条目会被扔掉。
  - **因为Python不支持方法的重载** functools.singledispatch 装饰器可以把整体方案拆分成多个模块，甚至可以为你无法修改的类提供专门的函数。使用@singledispatch 装饰的普通函数会变成泛函数（generic function）：根据第一个参数的类型，以不同方式执行相同操作的一组函数。

  ```python
  from functools import singledispatch
  from collections import abc
  import numbers
  import html
  @singledispatch ➊
  def htmlize(obj):
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)
  @htmlize.register(str) ➋
  def _(text): ➌
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{0}</p>'.format(content)
  @htmlize.register(numbers.Integral) ➍
  def _(n):
    return '<pre>{0} (0x{0:x})</pre>'.format(n)
  @htmlize.register(tuple) ➎
  @htmlize.register(abc.MutableSequence)
  def _(seq):
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'
  ```
- 参数化装饰器
  参数化装饰器是指实现对装饰器的传参一般在原先基础上再实现一层嵌套

  ```python
  def Wrapper(outer_param):
      def decorate(func):
          def inner(*args):
            """
              内部逻辑
            """
          return func
      return inner
    return decorate
  ```

## 对象引用，可变性和垃圾回收
- == 运算符比较两个对象的值（对象中保存的数据），而 is 比较对象的标识。

- **元组的相对不可变性** ： 元组与多数 Python 集合（列表、字典、集，等等）一样，保存的是对象的引用。 如果引用的元素是可变的，即便元组本身不可变，元素依然可变。也就是说，元组的不可变性其实是指 tuple 数据结构的物理内容（即保存的引用）不可变，与引用的对象无关。

- 浅复制；
  - 对可变对象（如list）进行+=操作会就地改变对象。对不可变对象（如元组）进行+=操作会创建新的对象
  - 利用构造方法list() 和 list[:]都是对列表的潜复制

  ```python
    l1 = [3, [66, 55, 44], (7, 8, 9)]
    l2 = list(l1) # ➊
    l1.append(100) # ➋
    l1[1].remove(55) # ➌
    print('l1:', l1)
    print('l2:', l2)
    l2[1] += [33, 22] # ➍
    l2[2] += (10, 11) # ➎
    print('l1:', l1)
    print('l2:', l2)
  ```
  ![](https://ws1.sinaimg.cn/large/6af92b9fgy1fy8e1aqfngj20dk0e374y.jpg)
  > Python Tutor是一个可视化代码之行过程的网站

- 为任意对象实现深浅复制： copy()函数和copy模块的deepcopy可以实现浅复制和深复制（不共享引用）；但是deepcopy有时很耗时，最好实现对象的__copy__ 和__deepcopy__方法自定义复制行为

- 函数的参数作为引用时：
  - 函数可能会修改接收到的任何可变对象
  - **不要使用可变类型作为参数的默认值** (默认值在定义函数时计算（通常在加载模块时），因此默认值变成了函数对象的属性。因此，如果默认值是可变对象，而且修改了它的值，那么后续的函数调用都会受到影响。)最好默认为None
  - 对于类的方法，除非这个方法确实想修改通过参数传入的对象，否则在类中直接把参数赋值给实例变量之前一定要三思，因为这样会为参数对象创建别名。如果不确定，那就创建副本。这样客户会少些麻烦。

- del和垃圾回收
  - del 语句删除名称，而不是对象。del 命令可能会导致对象被当作垃圾回收，但是仅当删除的变量保存的是对象的最后一个引用，或者无法得到对象时。
  - 在 CPython 中，垃圾回收使用的主要算法是**引用计数**。实际上，每个对象都会统计有多少引用指向自己。当引用计数归零时，对象立即就被销毁：CPython 会在对象上调用 __del__ 方法（如果定义了），然后释放分配给对象的内存。

- 弱引用 弱引用不会增加对象的引用数量。引用的目标对象称为所指对象（referent）。因此我们说，弱引用不会妨碍所指对象被当作垃圾回收。弱引用在缓存应用中很有用，因为我们不想仅因为被缓存引用着而始终保存缓存对象。可以用**weakref.ref**获取引用对象

## Ch9 Python风格的对象
- 自定义构造类
  - __iter__ 使得类实例变为可迭代对象进而可以进行**拆包**操作。 此方法可以简单地定义成生成器
  - __str__ __repr__ 定义类的描述
  - __bytes__ 定义返回字节形式 与bytes()函数对应
  - __eq__ 定义比较方式
  - __hash__ 使对象可散列（不可变）

- @classmethod 和 @staticmethod
  - classmethod 改变了调用方法的方式，因此类方法的第一个参数是类本身，而不是实例。classmethod 最常见的用途是定义备选构造方法
  - staticmethod 就是普通的静态方法

- python类的私有属性用__x双下划线定义，其实是实现了改名机制；也有约定俗称地用_x单下划线表示私有属性

- __slots__ 节省内存机制；在类中定义 __slots__ 属性的目的是告诉解释器：“这个类中的所有实例属性都在这儿了！”这样，Python 会在各个实例中使用类似元组的结构存储实例变量，从而避免使用消耗内存的 __dict__ 属性。如果有数百万个实例同时活动，这样做能节省大量内存。
如果你的程序不用处理数百万个实例，或许不值得费劲去创建不寻常的
类，那就禁止它创建动态属性或者不支持弱引用。与其他优化措施一
样，仅当权衡当下的需求并仔细搜集资料后证明确实有必要时，才应该
使用 __slots__ 属性。

## ch10 序列类型的修改、散列和切片
> 把协议当做非正式的接口

- 协议和鸭子类型；协议是非正式的，没有强制力，因此如果你知道类的具体使用场景，通常只需要实现一个协议的部分。例如，为了支持迭代，只需实现__getitem__ 方法，没必要提供 __len__ 方法。

- __getitem__ 实现切片的原理其实是讲index转换为slice对象，据此我们可以改写__getitem__ 使得对象切片后返回的仍然是对象（而不是数组）；
> my_seq[a : b : c] 句法背后的工作原理：创建
slice(a, b, c) 对象，交给 __getitem__ 方法处理。了解这一点之
后，我们让 Vector 正确处理切片，像符合 Python 风格的序列那样返回
新的 Vector 实例。

- 动态存取属性; 简单来说，对 **my_obj.x** 表达式，Python 会检查 my_obj 实例有没有名为 x 的属性；如果没有，到类（my_obj.__class__）中查找；如果还没有，顺着继承树继续查找。 如果依旧找不到，调用 my_obj 所属类中定义的__getattr__ 方法，传入 self 和属性名称的字符串形式（如 'x'）； 实现__setarr__ 方法可以进行属性赋值；

- 散列和快速等值测试
  - __hash__ + __eq__ 方法可以将对象变为可散列的；
  - __eq__ 可以采用些技巧使得对比更有效率

## ch11 接口：从协议到抽象基类
- 接口是对象公开方法的子集，让对象在系统中扮演特定的角色。Python 文档中的“文件类对象”或“可迭代对象”就是这个意思，这种说法指的不是特定的类。接口是实现特定角色的方法集合

- 对 Python 程序员来说，“X 类对象”“X 协议”和“X 接口”都是一个意思。

- 对象只要简单地实现了__getitem__方法就完成了序列协议， 可以取值、且切片、迭代、判断子元素等，尽管他没有实现ABC中的sequence的所有方法；但是这样的序列是不可变的，如果要实现可变序列，还要编写__setitem__方法。

- 抽象基类
  -  在 collections.abc 中，每个抽象基类的具体方法都是作为类的公开接口实现的，因此不用知道实例的内部接口。

    ![](https://ws1.sinaimg.cn/large/6af92b9fgy1fya27ecg4mj20ia0an76z.jpg)
  - numbers包是数字的抽象基类， 如检查类型： isinstance(x, numbers.Integral)

## ch12 继承的优缺点

- 直接子类化内置类型(如 dict、list 或 str)容易出错,因为内置类型的方法通常会忽略用户覆盖的方法。不要子类化内置类型,用户自己定义的类应该继承 collections 模块(http://docs.python.org/3/library/collections.html)中的类,例如UserDict、UserList 和 UserString,这些类做了特殊设计,因此易于扩展。
- 多重继承方法解析顺序
  - Python 会按照特定的顺序遍历继承图。这个顺序叫方法解析顺序(Method Resolution
    Order,MRO)。类都有一个名为 __mro__ 的属性,它的值是一个元组,按照方法解析顺序列出各个超类,从当前类一直向上,直到object 类。
  - 直接在类上调用实例方法时,必须显式传入 self 参数,因为这样访问的是未绑定方法(unbound method)。(**绕过MRO模式**)然而,使用 super() 最安全,也不易过时。调用框架或不受自己控制
    的类层次结构中的方法时,尤其适合使用 super()。

## ch13 正确重载运算符

## ch14 可迭代对象、迭代器和生成器

- 序列可以迭代的原因:iter函数

  - (1) 检查对象是否实现了 __iter__ 方法,如果实现了就调用它,获取一个迭代器。

  - (2) 如果没有实现 __iter__ 方法,但是实现了 __getitem__ 方法,Python 会创建一个迭代器,尝试按顺序(从索引 0 开始)获取元素。
  - (3) 如果尝试失败,Python 抛出 TypeError 异常,通常会提示“C objectis not iterable”(C 对象不可迭代),其中 C 是目标对象所属的类。
  - 任何 Python 序列都可迭代的原因是,它们都实现了 __getitem__ 方法。其实,标准的序列也都实现了 __iter__ 方法,因此你也应该这么做。之所以对 __getitem__ 方法做特殊处理,是为了向后兼容,而未来可能不会再这么做(不过,python3.4还未弃用)

- 可迭代对象与迭代器的对比

  - 明确可迭代的对象和迭代器（__iter__方法返回迭代器）之间的关系:**Python 从可迭代的对象中获取迭代器。**

  - 标准的迭代器接口有两个方法。

    - __next__返回下一个可用的元素,如果没有元素了,抛出 StopIteration异常。

    - __iter__返回 self,以便在应该使用可迭代对象的地方使用迭代器,例如在 for 循环中。

  - ![](https://ws1.sinaimg.cn/large/6af92b9fgy1fyczg3q6rjj20jd0csq4z.jpg)

  - 可迭代的对象有个 __iter__ 方法,每次都实例化一个新的迭代器;而迭代器要实现 __next__ 方法,返回单个元素,此外还要实现 __iter__  方法,返回迭代器本身。因此,**迭代器可以迭代,但是可迭代的对象不是迭代器。**

  - __iter__ 方法可以定义为生成器函数，最好不要返回一个迭代器对象；

- 标准库中的生成器函数

  - itertools.compress(it, selector_it) 并行处理两个可迭代对象：如果selector_it中的元素是真，产出it中对应的元素
  - itertools.dropwhile(predicate, it)处理it, 跳过产出剩下的各个元素（不再进行进一步检查）
  - filter(predicate, it)  Python3中的内置函数filter改为返回生成器对象
  - Itertools.filtefalse(predicate, ir) 与filter函数的逻辑相反， predicate为假时返回元素
  - itertools.islice(it,start, stop, step) 安生it的惰性切片
  - itertools.takewhile(predicate , it) pre为真时产出对应的元素，然后立即停止，不做继续检查
  - itertools.accumulate(it, [func]) 产出累计的总和； 如果提供了func , 那么吧前两个元素传给他，算计结果和下一个元素给他，以此类推
  - emumerate(it, start = 0) 
  - map(func , it)
  - itertools.starmap(func, it)  把it中各个元素传给func, 产出结果， It元素可为多个，以func(*iit)形式调用func
  - itertools.chain(it1, ..., itN) 先产出it1中的所有元素， 然后产出it2的元素，以此类推，无缝链接在一起
  - itertools.chain.from_iterable(it) 产出it生成的各个可迭代对象中的元素，无缝链接在一起； it 应该产出可迭代的元素，例如可迭代的对象列表
  - itertools.product(it1, ..., itN, repaeat = 1) 计算**笛卡尔积**
  - zip(it1, ...., itN)
  - zip_longest(it1, ... , itN ,fillvalue = None)
  - itertools.combinations(it, out_len) 把it产出的out_len个元素组合在一起，然后产出 ; 做$C_m^n$ **组合数逻辑**
  - itertools.count(start =0, step =1) 无中生有函数
  - itertools.cyle(it)从It中产出 各个元素，存储各个元素的副本，然后按顺序重复不断产出各个元素
  - itertools.permutations(it, out_len = None) 吧out_len个it产出的元素排列在一起，然后产出这些排列；**Amn, 排列数逻辑**
  - itertools.repeat(item , [times])
  - itertools.groupby(it, key = None) 产出由两个元素组成的元素，形式为(key, group) , 其中key是分组标准， group 是生成器， 用于财产出分组里的元素
  - reversed(seq) 
  - itertools.tee(it, n= 2) 产出一个由n个生成器组成的元素，每个生成器用于单独产出输入的可迭代对象中的元素

  > 注意,这一节的示例多次把不同的生成器函数组合在一起使用。这是这些函数的优秀特性:这些函数的参数都是生成器,而返回的结果也是生成器,因此能以很多不同的方式结合在一起使用

- yield from 句法 : 使得生成器函数产出另一个生成器生成的值，避免了嵌套for循环

## ch15  上下文管理和else模块

- for/else、while/else 和 try/else 中的else的作用更接近与then 的意思
- with 语句的目的是简化 try/finally 模式。这种模式用于保证一段代码运行完毕后执行某项操作,即便那段代码由于异常、return 语句或sys.exit() 调用而中止,也会执行指定的操作。finally 子句中的代码通常用于释放重要的资源,或者还原临时变更的状态。 
- 上下文协议需要实现__enter__ 和 __exit__ 方法
- @contextlib.contextmanager 装饰器能减少创建上下文管理器的样板代码量,因为不用编写一个完整的类,定义 __enter__ 和 __exit__ 方法,而只需实现有一个 yield 语句的生成器,生成想让 __enter__ 方法返回的值。

## ch16 协程 （Coroutines）

- 定义：（生成器进化为协程）yield 关键字可以在表达式中使用,而且生成器 API 中增加了 .send(value) 方法。生成器的调用方可以使用 .send(...) 方法发送数据,发送的数据会成为生成器函数中 yield 表达式的值。因此,生成器可以作为协程使用。协程是指一个过程,这个过程与调用方协作,产出由调用方提供的值。

- ![](https://ws1.sinaimg.cn/large/6af92b9fgy1fyd6auknuoj20jg09r781.jpg) 

  先执行yield等号右边

- 示例：计算移动平均

  ```python
  def averager():
      total = 0.0
      count = 0
      average = None
      while True: ➊
          term = yield average ➋
          total += term
          count += 1
          average = total/count
  ```

- 预激协程的装饰器

  调用协成第一步要先激活，即执行yield语句之前的程序。 因此可以编写预激协程的装饰器，但注意要与yield from兼容

- 生成器对象可以调用throw() 和 close() 方法发送异常给协程

- yield from x 表达式对 x 对象所做的第一件事是,调用 iter(x),从中获取迭代器。因此,x 可以是任何可迭代的对象； yield from 的主要功能是打开双向通道,把最外层的调用方与最内层的子生成器连接起来,这样二者可以直接发送和产出值,还可以直接传入异常,而不用在位于中间的协程中添加大量处理异常的样板代码。有了这个结构,协程可以通过以前不可能的方式委托职责。

## ch17 使用期物处理并发

- concurrent.futures 模块的主要特色是 ThreadPoolExecutor 和ProcessPoolExecutor 类,这两个类实现的接口能分别在不同的线程或进程中执行可调用的对象。这两个类在内部维护着一个工作线程或进程池,以及要执行的任务队列。
- **GIL 几乎对 I/O 密集型处理无害**:(解释了虽然Python多线程不是真正意义上的多线程，但是在IO密集操作上仍能加速的原因)； 标准库中所有执行阻塞型 I/O 操作的函数,在等待操作系统返回结果时都会释放 GIL。这意味着在 Python 语言这个层次上可以使用多线程,而 I/O 密集型 Python 程序能从中受益:一个 Python 线程等待网络响应时,阻塞型 I/O 函数会释放 GIL,再运行一个线程。
- futures模块的ProcessPoolExecutor 和 ThreadPoolExecutor 类都实现了通用的Executor 接口,因此使用 concurrent.futures 模块能特别轻松地把基于线程的方案转成基于进程的方案； Process适合**CPU密集型**程序， 而多线程 适合**IO 密集型**程序

## ch18 使用asyncio处理并发

