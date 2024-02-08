# 汽车造型设计文件管理系统
## 概述
整个项目的目标分成两个部分

# 第一部分 - 文件自动管理系统

## 需求来源

我每天都需要面对**大量的信息输入**：开各种会，接收各种文件，有各种各样的临时性任务和长期性的任务。在处理这些任务的过程中，也会产生各种各样的临时性的文件，这些信息有的对于我有挺大的价值，很有可能会在短时间内被重新调取，比如两三天，但也有可能是两三个月之后，两三周以内的文件，我可能还能努力找到，但超过一个月的文件，其实根据人的记忆原则就很难再找到了。

因此，我想开发一个这样的文件管理系统，能够帮我快速归档文件，一方面是用电脑的逻辑帮我记忆，另一方面也是使用电脑的逻辑来帮我自己进行文件的整理。这边的第二个概念的意思是，我自己其实对文件的归档没有特别深刻的想法，通过对文件归档逻辑的思考和编程，也能帮助我结构化处理我每天所面临的大量数据和信息，而不是简单地把他们按照几种文件夹路径进行归档。我相信这个思路背后涉及到的不仅仅是常见的计算机知识，也涉及到人脑记忆、信息处理、信息调取等知识，我需要有一个所谓的“**第二大脑**”，在我本人和计算机之间建立起一座更深更快速的桥梁，它不仅仅帮我记忆，同时根据我的逻辑、我的世界观进行记忆、根据我的偏好进行信息的搜集、
**注意力**的集中，也就是说，这个系统关注什么信息，如何对信息进行过滤和处理，其实都是根据我自己的经验和逻辑进行的。

借助这个项目，我希望能系统性地训练自己从**信息和数据的视角看待自己的工作内容**，比如：
- 如何对日常的任务进行归档，收到任务之后，应该做哪些信息处理？有没有尽可能地系统化？
- 从信息科学和数据库管理的视角，我当前工作的相关内容属于什么

借助这个项目，我希望能够自动整理输入文件，自动对输入信息进行清洗和归档。比如自动归档“下载”“桌面”等容易杂乱的文件夹。

借助这个项目，我希望对已有的过往项目文件进行系统性的自动化处理。


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



