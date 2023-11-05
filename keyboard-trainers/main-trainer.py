import pygame
import time
import random

class KeyboardTrainer:
    def __init__(self, tasks_file, statistics_file): # Обработка файлов
        self.sentences = self.load_sentences(tasks_file)
        self.statistics = self.load_statistics(statistics_file)

    def load_sentences(self, file_name): # Чтение файла с текстом
        with open(file_name, 'r') as file:
            tasks_data = file.read()
        sentences = tasks_data.split('\n')
        return sentences

    def load_statistics(self, file_name): # Чтение файла с статистикой
        try:
            with open(file_name, 'r') as file:
                statistics_data = file.read()
                statistics = statistics_data.splitlines()
                total_errors, total_time, total_attempts, total_averrors = map(float, statistics)
        except FileNotFoundError:
            total_errors = 0
            total_time = 0
            total_attempts = 0
            total_averrors = 0
        return {'total_errors': total_errors, 'total_time': total_time, 'total_attempts': total_attempts, 'total_averrors': total_errors / total_attempts}

    def save_statistics(self, file_name): # Запись статистики в файл, в случае его отсутсвия, создает такой файл
        with open(file_name, 'w') as file:
            statistics_data = [str(self.statistics['total_errors']), str(self.statistics['total_time']), str(self.statistics['total_attempts']), str(self.statistics['total_averrors'])]
            file.write('\n'.join(statistics_data))

    def calculate_wpm(self, input_string, time_diff): # Подсчет скорости печати
        words_typed = len(input_string.split())
        minutes_diff = time_diff / 60
        wpm = words_typed / minutes_diff
        return wpm

    def reset_statistics(self): # Обнуление статистики
        self.task = random.choice(self.sentences)
        self.lentask = len(self.task)
        self.index = 0
        self.input_string = ""
        self.errors  = 0
        
    def run(self): # Главная функция
        W = 800
        H = 600
        wpm = 0
        
        pygame.init()
        
        screen = pygame.display.set_mode((W, H)) # Создание дисплея
        pygame.display.set_caption('Keyboard-trainer')
        
        bg = pygame.image.load('background.jpg') # Создание фона
        bg = pygame.transform.scale(bg, (W,H))
        
        font = pygame.font.Font(None, 36) # Размер шрифта
        self.reset_statistics()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Завершение
                    pygame.quit()
                    return

                elif event.type == pygame.KEYDOWN:
                    if event.unicode == self.task[-1] and self.index == self.lentask - 1: # Правильный ввод последнего символа
                        end_time = time.time() # Завершаем считать время
                        
                        time_diff = end_time - start_time
                        wpm = self.calculate_wpm(self.input_string, time_diff) # Считаем скорость

                        self.statistics['total_errors'] += self.errors
                        self.statistics['total_time'] += time_diff
                        self.statistics['total_attempts'] += 1

                        self.save_statistics('statistics.txt')  # Сохранение статистики
                        
                        self.reset_statistics()

                    elif event.key == pygame.K_BACKSPACE: # Если удаляется символ какой то
                        input_string = input_string[:-1]
                        self.index -= 1

                    else: # Если вводим какой то символ
                        if self.input_string == "":
                            start_time = time.time()
                        if event.key == pygame.K_LSHIFT or  event.key == pygame.K_LSHIFT:
                            self.errors -= 1
                        if event.unicode == self.task[self.index]: # Если вводим правильный символ
                            self.index += 1
                            self.input_string += event.unicode
                        else:
                            self.errors += 1
            screen.blit(bg, (0,0)) # Создаем текст на нашем дисплее
            task_text = font.render(f"Выведете: {self.task}", True, (0, 0, 0))
            screen.blit(task_text, (10, 10))
            input_text = font.render(f"Строка ввода: {self.input_string}", True, (150, 0, 0))
            screen.blit(input_text, (10, 50))
            err = font.render(f"Ошибки: {self.errors}", True, (0, 0, 0))
            screen.blit(err, (10, 100))
            WPM = font.render(f"Скорость печати (WPM): {wpm}", True, (0, 0, 0))
            screen.blit(WPM, (10, 150))
            
            pygame.display.flip()


if __name__ == '__main__': # Чтобы при импорте не срабатывала сразу
    trainer = KeyboardTrainer('tasks.txt', 'statistics.txt')
    trainer.run()