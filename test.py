# # import time
# # for i in range(10):
# #     time.sleep(0.4)
# #     print('\r',str(10-i).ljust(50),end='')
# import threading

# def print_message(message):
#     print("Thread:", threading.current_thread().name, "Message:", message)

# if __name__ == '__main__':
#     threads = []
    
#     for i in range(5):
#         thread = threading.Thread(target=print_message, args=("Hello World!",))
#         thread.start()
#         threads.append(thread)
    
#     for thread in threads:
#         thread.join()
import threading
import time
import curses

# 初始化 curses
stdscr = curses.initscr()
curses.curs_set(0)  # 隐藏光标

# 创建两个窗口，一个用于第一行，一个用于第二行
win1 = stdscr.subwin(1, curses.COLS, 0, 0)
win2 = stdscr.subwin(1, curses.COLS, 1, 0)

# 线程函数，第一个线程在第一行刷新显示，第二个线程在第二行刷新显示
def refresh_thread1(win):
    while True:
        win.clear()
        win.addstr("线程1: 刷新显示在第一行")
        win.refresh()
        time.sleep(1)

def refresh_thread2(win):
    while True:
        win.clear()
        win.addstr("线程2: 刷新显示在第二行")
        win.refresh()
        time.sleep(1)

# 创建线程
thread1 = threading.Thread(target=refresh_thread1, args=(win1,))
thread2 = threading.Thread(target=refresh_thread2, args=(win2,))

# 启动线程
thread1.start()
thread2.start()

# 等待线程结束
thread1.join()
thread2.join()

# 恢复终端设置
curses.endwin()
