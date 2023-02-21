import gym
import random

env = gym.make("CartPole-v1", render_mode="rgb_array")


def Random_games():
    # Каждый из этих эпизодов - это своя собственная игра.
    for episode in range(0,10):
        env.reset()
        # это каждый кадр, до 500...но с рэндомом мы так далеко не продвинемся.
        for t in range(0,500):
            # Это отобразит окружающую среду
            # Показывайте только в том случае, если вы действительно хотите это увидеть.
            # Для его отображения требуется гораздо больше времени.
            env.render()

            # Это просто создаст пример действия в любой среде.
            # В этой среде действие может быть 0 или 1, то есть левым или правым
            action = env.action_space.sample()

            # это выполняет среду с действием,
            # и возвращает наблюдение за средой,
            # вознаграждение, если env закончен, и другую информацию
            next_state, reward, done, info = env.step(action)

            # давайте напечатаем все в одной строке:
            print(t, next_state, reward, done, info, action)
            if done:
                break


Random_games()
