## 登录页面总要求

编写一个用户注册页面，提供外部用户注册。为此需要再设计一个空index页面，并且有一个sign in的按钮，用户点击sign in按钮之后，跳转到注册页面，填写信息并提交后返回index页面。

### 需求

1. 需要用户填写的信息及要求：

   | label        | 对应数据库字段名 | 要求                                                         |
   | ------------ | ---------------- | ------------------------------------------------------------ |
   | UserNama     | LoginName        | 不能为空，与数据库中用户名不重复，可以包含数字，字母，下划线；不能包含空格和特殊字符 |
   | Password     | LoginPasswd      | 不能为空，至少8个字符，最多25个字符，必须且只能包含小写字母， 大写字母，数字，特殊字符中的三种及以上 |
   | RealName     | RealName         | 非必填，其他要求同username                                   |
   | Email        | Email            | 必填，需要判断是否为邮箱格式（必要时，使用邮件验证其真实性，验证这一步非必须，但需要提示用户，此邮箱用于接收后续一系列信息，需填常用邮箱) |
   | Phone        | Phone            | 非必填，只能由数字与+组成                                    |
   | District     | District         | 必填，可做成下拉框选择                                       |
   | Country      | Country          | 必填，如上                                                   |
   | City         | City             | 必填，如上                                                   |
   | Organization | Organization     | 必填，可填缩写                                               |

2. 其他需求：
   1. 当用户填写的信息不符合要求时，及时出现提示信息提示用户；
   2. 用户填写的信息不符合要求时，点击提交按钮无效；
   3. 用户填写的信息都满足要求，并且点击提交后，将用户信息添加到数据库中；
   4. 使用root.css中的配色；
   5. 推荐使用表单(Form)来实现；
   
3. 用户角色定义：

   | 用户角色id | 角色名        | 说明                                             |
   | ---------- | ------------- | ------------------------------------------------ |
   | 1          | Guest         | 只注册了系统，未购买芯片也未被分配芯片的普通用户 |
   | 2          | Partner       | 未购买芯片，但被分配了芯片                       |
   | 3          | Customer      | 购买了芯片的用户                                 |
   | 4          | Analyst       | 数据分析员                                       |
   | 5          | Productor     | 芯片生产者                                       |
   | 6          | Developer     | 系统开发者                                       |
   | 7          | Administrator | 系统管理员                                       |


__8月18号待修改__

1. __样式调整，请调整成如下样式（类似）：__

![1597732861843](E:\06.git\stereo_signin\assets\login.png)

_说明如下:_

	* 表单的className包含‘login_form’
	* 表单内直接子元素的className包含 ‘input_part’
	* 表单中button的className包含‘login_button’
	* 表单中每个输入框和下拉框保持相同的高度和宽度


2. __关于提示信息__：

   * username和password的规则需要写在input下面，用于提示用户
   * 其他所有的提示信息放在一起，不需要每一个input后面都有提示
   * input中信息填写正确时不需要出现提示
   * 没有验证邮箱格式，用户填写错误的邮箱格式也可以通过验证，请增加邮箱格式的验证

3. __关于地址选择__:

   问题描述：地区，国家，省市被清除后，会报错，同时有些地区没有到city层级，则用户永远验证不过

   解决思路：动态生成下一层级的下拉框

4. __关于Form__：

   * 整个注册页面应该保持一个form表单，目前每一个input外面都包裹了一个表单是不合理的
   * 注意表单中的button的type属性，默认为‘submit’，如不需要，可修改为‘button’

5. __关于正则表达式__：

   * username是可以下划线开头的，目前的正则中没有匹配下划线和数字开头的情况，可以统一使用如下正则表达式：`^[0-9a-zA-Z_]+$`
   * password的正则是对的，可以统一使用如下简约的写法：`^(?=.*[a-zA-Z])(?=.*[1-9])(?=.*[\W]).{8,25}$ ` (同时包含字母，数字，特殊符号)



## stat页面总要求

根据结果文件`./data/test_stat/`生成html报告，报告样式可以参考 `./data/example.html`。

### 需求

1. 可以使用Tab实现，json文件中第一层的key作为Tab的标签名，标签页中，可以使用下拉框来选择不同的样本或者不同的bin size来展示其相关信息；

2. 每个标签页中重点突出的数据为：

   | 标签名         | 重点指标名          |
   | -------------- | ------------------- |
   | Filter and Map | mapped_reads        |
   |                | clean_reads         |
   | Alignment      | Mapped_reads        |
   |                | Unique_reads        |
   |                | Duplication_rate    |
   | Basic          | Umi_Counts_Per_Bin  |
   |                | Gene_Counts_Per_bin |

3. 图片需要对应上不同的bin size页面

4. 过滤结果的报告以链接展示

Note：样本数目可能会增加和减少，bin size的数目也可能会增加和减少，需要能适配。可以尝试使用dash_bootstrap_components来实现



## 用户下单需求

1. 需求描述：
   1. 用户填写购买需求；
   2. 提交后邮件给经理并在系统提醒经理审核
   3. 审核通过后，提醒用户付款/签合同等操作，并上传凭证
   4. 通知生产部门，生产芯片产品
   5. 芯片分配给用户的订单

2. 原设计：
   1. 下单流程设计
   
    ![下单流程](E:\06.git\stereo_signin\assets\下单流程.png)
   
   2. 提报单状态

    ![提报单状态](E:\06.git\stereo_signin\assets\提报单状态.png)

3. __根据以上需求设计数据库表格和页面__

