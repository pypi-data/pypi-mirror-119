<div align="center">
  <img src="docs/imgs/logo.jpg" height="240" />
</div>

[![Anaconda-Server Badge](https://anaconda.org/jdgalileo/jdgalileo/badges/version.svg)](https://anaconda.org/jdgalileo/jdgalileo)

Galileo（伽利略）是一个图深度学习框架，具备超大规模、易使用、易扩展、高性能、双后端等优点，旨在解决超大规模图算法在工业级场景的落地难题，提供图嵌入和图神经网络模型的训练评估及预测能力。

# 架构介绍

<div align="center">
    <img src="docs/imgs/arch.png" height="450" /><br/>
    Galileo整体架构
</div>

Galileo图深度学习框架采用分层设计理念，主要分为分布式图引擎、图多后端框架、图模型三层。
- **分布式高性能图引擎**：采用紧凑高效的内存结构表达图数据，能够以极低有内存支持**超大规模异构图**；基于ZeroCopy机制实现全链路调用，高性能图查询和图采样。
- **图多后端框架**：支持Tensorflow和PyTorch双后端，配置化单机分布式训练，支持Keras和Esitmator训练，提供统一的图查询和图采样接口**易扩展**。
- **图模型**：遵循数据与模型解耦，提升代码复用性；基于组件化设计，降低模型实现难度，支持Message Passing范式编写图模型，也支持Python直接访问训练后端接口，**易使用且灵活性高**。


# 开始使用
推荐使用[pip或conda](docs/pip.md)安装Galileo，高级用户可以从[源码编译安装](docs/install.md)Galileo。

阅读[入门教程](docs/introduce.md)开始使用Galileo。

如果Galileo目前实现的[图模型](examples/README.md)无法满足需求，可以[定制化图模型](docs/custom.md)。

使用自己的图数据可以参考[图数据准备](docs/data_prepare.md)。

如果图数据量大，可以参考[分布式训练](docs/train.md)。

想要了解更多Galileo接口参考[API文档](docs/api.md)。


# 联系我们
欢迎通过issue和邮件组（galileo_opensource@jd.com）联系我们。

# LICNESE
Galileo图深度学习框架使用Apache License 2.0许可。

# 致谢
Galileo图深度学习框架由京东集团-京东零售-技术与数据中心荣誉出品，在此感谢京东零售算法通道的大力支持，同时感谢商业提升事业部、搜索与推荐平台部等兄弟部门在开发及使用过程中提的宝贵意见。

