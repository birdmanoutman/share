# 汽车造型设计文件管理系统
## 概述
整个项目的目标分成两个部分

# 第一部分 - 汽车造型设计策略文档管理与生产系统

## 需求来源
### 信息输入
我每天都需要面对**大量的信息输入**：开各种会，接收各种文件，有各种各样的临时性任务和长期性的任务。在处理这些任务的过程中，也会产生各种各样的临时性的文件，有的信息对我有挺大的价值，很有可能会在短时间内被重新调取，比如两三天，但也有可能是两三个月之后，两三周以内的文件，我可能还能努力找到，但超过一个月的文件，就很难再找到了。
因此，我想开发一个这样的生产系统，能够帮我快速归档文件。这个生产系统一方面是帮我记忆，另一方面也是使用电脑的逻辑来帮我自己进行文件的整理。这边的第二个概念的意思是，我自己其实对文件的归档没有特别深刻的想法，通过对文件归档逻辑的思考和编程，也能帮助我结构化处理我每天所面临的大量数据和信息，而不是简单地把他们按照几种文件夹路径进行归档。我相信这个思路背后涉及到的不仅仅是常见的计算机知识，也涉及到人脑记忆、信息处理、信息调取等知识，我需要有一个所谓的“**第二大脑**”，在我本人和计算机之间建立起一座更深更快速的桥梁，它不仅仅帮我记忆，同时根据我的逻辑、我的世界观进行记忆、根据我的偏好进行信息的搜集、
**注意力**的集中，也就是说，这个系统关注什么信息，如何对信息进行过滤和处理，其实都是根据我自己的经验和逻辑进行的。

借助这个项目，我希望能系统性地训练自己从**信息和数据的视角看待自己的工作内容**，比如：
- 如何对日常的任务进行归档，收到任务之后，应该做哪些信息处理？有没有尽可能地系统化？
- 从信息科学和数据库管理的视角，我当前工作的相关内容属于什么

借助这个项目，我希望能够自动整理输入文件，自动对输入信息进行清洗和归档。比如自动归档“下载”“桌面”等容易杂乱的文件夹。
借助这个项目，我希望对已有的过往项目文件进行系统性的整理，对过往的所有项目和任务进行结构化。

参考视频：
>[为什么你不需要"第二大脑"](https://www.youtube.com/watch?v=5kNCcpM61eo)
>
> P.A.R.A 不是文件系统，是生产系统，tiago forte, Building a Second Brain

>[我是如何快速学习一个领域的](https://www.bilibili.com/video/BV11o4y1s7VY/?spm_id_from=333.337.search-card.all.click&vd_source=1d47a8c44e1d0084ecf47d3631b7e45a)

>[把知识变成资产: 作为知识博主,我是如何研究一个话题的](https://www.youtube.com/watch?v=MvFIFoKqfus&list=LL&index=8&t=622s)

>两种项目类型：
-P_Sprint
-P_SlowBrun

code 服务流程
para 服务结构
强调actionability

信息收集和整理的核心目的：面向我要解决的问题，为信息找到明确的归宿



## 整体思路
1. 高质量的信息生成与高质量的信息存储
   避免garbage in garbage out，做到Garbage In, Resource Out；
   规范数据采集和录入。
   数据清洗和预处理：对数据进行清洗和预处理，**去除无效数据、异常值和重复数据**，确保数据的准确性和完整性。
   数据验证和校验：在数据输入和处理过程中实施验证和校验机制，确保数据符合规范和要求。
2. 目录结构设计
   通过项目文件夹（对象）和数据文件夹（对象）对所有的文件数据进行管理。项目对象是时间维度的，数据是
   
## 目录基本结构
- PROJECTS
   - SAIC
      - DS研究
      - DS沟通
      - DS稿件
   - 
- DATA
   - IMG
   - TXT
   - VIDEO
   - AUDIO
   - OTHER
   - 3D
   - TRASH

## 文件格式自动归类模块

1. 文件根据格式自动分模块
    - autoFormatClassfication.py
    - 输入文件夹路径，结合json文件内容，对这个文件夹里的文件进行自动归类到对应文件夹中
    - 当用户没有输入要整理的路径时，脚本将自动使用默认路径（桌面）；配置路径没有输入时候也使用默认

2. 文件类型配置json文件
    - file_categories.json
    - 用于配置文件管理系统的文件分类格式，TXT文件夹映射有：pdf,txt,docx,等文本类型的文件;IMG文件夹映射:
      png,jpg,psd,ai,webp等文件，AUDIO映射各类音频文件；VEDIO映射各类视频文件格式；3D映射各类三维文件格式；

## 标记与类别

## 文件夹自动规范命名模块
1. 需求描述：
   - 原则上，涉及到工作内容的文件夹，都应该规范命名。参考过往的案例，一般命名规则是YYMMDD_项目名称
   - 归档逻辑，服务（汇报）对象，项目类型，汇报对象，项目类型依次递归
2. 文件夹归档组织：
- 项目类（Project）：
   - 设计研究
   - 设计沟通
   - 设计实践
- 数据类（Data）：
   -    

## 会议纪要整理模块

## notion同步

我希望快速读取notion数据库， 建立本地文件夹和notion数据库的百分之百同步。
TXT表作为一个关系，他的Title为在dell本地电脑上的路径，同时还有两个属性记录了这些文件在mac电脑和frp创建的http文件服务的路径。
检查notion数据库，如果数据库中的Tile条目是一个页面而不是一个链接，那么就把这个页面转化为一个markdown文件保存在本地文件的特定路径上，同时title就用这个路径文本替换

# 自然语言编程内容
我要写一个python程序，能够帮我实现自动归档特定文件夹下的所有内容。输入是要归档文件夹的路径，运行程序后，程序能够自动将路径下的所有文件进行规定好的逻辑进行归档。
目标归档文件夹下包含两个文件夹，第一个文件夹叫做"projects"，第二个文件夹叫做"data"。
project文件夹下面包含各种项目文件，是用户根据实际项目名称自己创建的文件夹；而data有自动生成的文件夹，包含"TXT"（文本数据），"IMG"（图像数据），"MP3"（音频数据），"3D"（三维数据），"OTHER"（其它，如压缩包等）。

整理一个文件夹时，需要逐一地分析每一个文件的内容，文字内容可以通过openAI_api进行分析，

高质量信息处理与管理原则：
- 输入的信息，就应该是高质量的。


TXT文本类文件：
简单任务:
.docx; 
判断docx是文字还是图片
.txt; .py;


# 任务类型
## OD计算
## 抠图
## 信息搜集
### 网络信息
### 








