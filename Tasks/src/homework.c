#include "homework.h"
#include "homework_config.h"

extern TIM_HandleTypeDef htim2;
extern IWDG_HandleTypeDef hiwdg;

volatile uint32_t tick = 0;

void Homework_Init(void)
{
  /* The F103 board LED is active low. */
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
  if (HAL_TIM_Base_Start_IT(&htim2) != HAL_OK)
  {
    Error_Handler();
  }
}

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
  if (htim->Instance == TIM2)
  {
    ++tick;
#if HOMEWORK_FEED_IWDG
    HAL_IWDG_Refresh(&hiwdg);
#endif
  }
}
