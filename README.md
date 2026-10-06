# STM32F103C8T6 电控第一次作业

同一个 STM32CubeMX CMake 工程完成 GPIO、TIM2 定时器和 IWDG。芯片型号为 STM32F103C8T6，板载 LED 在 PC13，SWD 调试器为 CMSIS-DAP。

## 工程结构

- `STM32F103_HW1.ioc`：CubeMX 配置；IWDG 一直启用。
- `CMakeLists.txt`：作业发放的 CMake 模板，`user_folders` 为 `"Tasks"`。
- `Tasks/src/homework.c`：PC13 初始化、`tick` 和唯一的 TIM2 更新回调。
- `Tasks/inc/homework_config.h`：用 `HOMEWORK_FEED_IWDG` 选择是否喂狗。
- `Core/`、`Drivers/`、`cmake/`：CubeMX/HAL 工程文件。
- `firmware/02_timer_feed.elf`：第二题已经单独构建和下载验证的版本。
- `firmware/03_watchdog_reset.elf`：第三题已经单独构建和下载验证的版本。
- [`作业说明.md`](作业说明.md)：计算过程、结果说明和附录图片。
- [`作业说明.pdf`](作业说明.pdf)：说明文档的阅读版本。

## 构建

使用 ARM GNU Toolchain、CMake 和 Ninja。先编辑 `Tasks/inc/homework_config.h`：

- `#define HOMEWORK_FEED_IWDG 1`：第二题，TIM2 每 1 ms 中断时刷新 IWDG。
- `#define HOMEWORK_FEED_IWDG 0`：第三题，编译时去掉刷新调用，IWDG 约 2 秒复位。

每次切换后分别运行：

```sh
cmake --preset Debug
cmake --build --preset Debug
```

两个版本分别下载到板上观察，不用同时运行。生成的 ELF 位于 `build/Debug/`。`firmware/` 保存了已经验证的两份 ELF，便于比对。

## 已验证的运行现象

- PC13 低电平，板载 LED 点亮。
- 喂狗版：Ozone Timeline 中 `tick` 持续增长，斜率约为每秒 1000；[截图](appendix/02_timer_ozone.png)。
- 不喂狗版：Ozone Timeline 中 `tick` 约每 2 秒从接近 2000 回到低值，再重新增长；[截图](appendix/03_watchdog_ozone.png)。

另保留 pyOCD 读取实际硬件 RAM 的[定时器](appendix/02_timer_pyocd.png)和[看门狗](appendix/03_watchdog_pyocd.png)截图作为补充记录。
