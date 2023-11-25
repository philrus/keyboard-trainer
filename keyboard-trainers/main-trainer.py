import pygame
import time
import random

# Используемые цвета
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (150, 0, 0)

# Класс отрисовывающий одну клавишу
class Key:
    def __init__(self, char, x, y, width, height):
        self.char = char
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        # Отрисовка клавиши
        pygame.draw.rect(surface, WHITE, self.rect, 0)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        # Отрисовка текста на клавише
        text_surface = self.font.render(self.char, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def highlight(self, surface, color):
        # Перекрашиваем клавишу
        pygame.draw.rect(surface, color, self.rect, 0)

        # Отрисовка текста на клавише
        text_surface = self.font.render(self.char, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class Keyboard:
    def __init__(self):
        self.keys = [] # Список с key - объекты класса Key
        
        # Размеры клавиатуры
        WIDTH = 800
        HEIGHT = 400
        
        # Параметры клавиатуры
        ROWS = 4
        COLS = 11
        
        key_width = WIDTH // COLS
        key_height = HEIGHT // ROWS
        KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-',
                'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '?',
                'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', ':',
                'Z', 'X', 'C', 'V', 'B', 'N', 'M',  '.', ',', '(', ')']
        
        for row in range(ROWS):  # Заполняем наш список каждой клавишей со своими параметрами
            for col in range(COLS):
                char = KEYS[row*COLS + col]
                x = col * key_width + 50
                y = row * key_height + 300
                key = Key(char, x, y, key_width, key_height)
                self.keys.append(key)

    def draw(self, surface): # Отрисовка каждой клавиши
        for key in self.keys:
            key.draw(surface)
            
    def highlight_key(self, char): # Возвращает клавишу, которую надо покрасить
        for key in self.keys:
            if key.char == char:
                return key

    def found_event(self, event): # Проверяет наличие нажатой клавиши на рисованной клавиатуре
        for key in self.keys:
            if key.char.lower() == event or key.char == event:
                return key.char

            
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
        W = 900
        H = 800
        wpm = 0
        pygame.init()

        screen = pygame.display.set_mode((W, H)) # Создание дисплея
        pygame.display.set_caption('Keyboard-trainer')

        bg = pygame.image.load('background.jpg') # Создание фона
        bg = pygame.transform.scale(bg, (W,H))
    
        font = pygame.font.Font(None, 36) # Размер шрифта
        self.reset_statistics()

        keyboard = Keyboard() # Создаем объект класса
        
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
                        self.input_string = self.input_string[:-1]
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
                            # Подсветка неправильно нажатой клавиши
                            char_error = keyboard.found_event(event.unicode) 
                            if char_error: # Проверяем, что данная клавиша есть в рисованой клавиатуре
                                highlighted_key1 = keyboard.highlight_key(char_error)
                                keyboard.draw(screen)
                                highlighted_key1.highlight(screen, YELLOW) # Красим в желтый
                                pygame.display.flip()
                                time.sleep(0.09)
    
                # Создаем текст на нашем дисплее
                screen.blit(bg, (0,0))
                task_text = font.render(f"Выведете: {self.task}", True, BLACK)
                screen.blit(task_text, (10, 10))
                input_text = font.render(f"Строка ввода: {self.input_string}", True, RED)
                screen.blit(input_text, (10, 50))
                err = font.render(f"Ошибки: {self.errors}", True, BLACK)
                screen.blit(err, (10, 100))
                WPM = font.render(f"Скорость печати (WPM): {wpm}", True, BLACK)
                screen.blit(WPM, (10, 150))

                keyboard.draw(screen) # Рисуем клавиатуру
            
                pygame.display.flip()
                
            # Подсветка правильно нажатой клавиши
            char_right = keyboard.found_event(self.task[self.index])
            highlighted_key2 = keyboard.highlight_key(char_right)
            highlighted_key2.highlight(screen, RED) # Красим в красный
            pygame.display.flip()

if __name__ == '__main__': # Чтобы при импорте не срабатывала сразу
    trainer = KeyboardTrainer('tasks.txt', 'statistics.txt')
    trainer.run()
