from lib.LogManager.LogManager import LogManager
import win32gui
import time
import os
import multiprocessing


class AlfarmAutomation:
    def __init__(self, alfarm_path: str):
        self.__loger = LogManager(real_time_mode=True)
        self.__alfarm_path = alfarm_path
        self.__detect_window_name = 'BlueStacks App Player'
        self.__detect_process_name = 'HD-Player.exe'
        self.__alfarm_hwnd = None
        return

    def print_interrupt_exit_log(self) -> None:
        time.sleep(1)
        self.__loger.update(real_time_mode=False)
        self.__loger.log('Exit the program because a keyboard interrupt was detected')
        return

    def __wait_for_window(self, wait_count: int = 10, wait_time: float = 5.0) -> int and bool:
        for i in range(wait_count):
            hwnd = win32gui.FindWindow(None, self.__detect_window_name)
            if hwnd:
                return hwnd, True
            else:
                time.sleep(wait_time)
        return None, False

    def __activate_window(self) -> None:
        win32gui.ShowWindow(self.__alfarm_hwnd, 5)
        win32gui.SetForegroundWindow(self.__alfarm_hwnd)
        return

    def __alfarm_runner(self) -> None:
        try:
            os.system(self.__alfarm_path)
        except KeyboardInterrupt:
            os.system(f'taskkill /F /IM {self.__detect_process_name}')
        return

    def __main_logic(self) -> None:
        try:
            self.__loger.log('Starting Alfarm...')
            self.__alfarm_hwnd, return_value = self.__wait_for_window()
            self.__activate_window()
            if return_value:
                self.__loger.log('Success')
            else:
                self.__loger.log('Failure')
            while True:
                pass
        except KeyboardInterrupt:
            os.system(f'taskkill /F /IM {self.__detect_process_name}')
        return

    def handler_logic(self, process_num: int) -> None:
        try:
            if process_num == 0:
                self.__alfarm_runner()
            else:
                self.__main_logic()
        except KeyboardInterrupt:
            os.system(f'taskkill /F /IM {self.__detect_process_name}')
        return

    def automation_logic(self) -> None:
        process_list = [0, 1]
        pool = multiprocessing.Pool()
        try:
            pool.map(self.handler_logic, process_list)
            pool.close()
            pool.join()
        except KeyboardInterrupt:
            self.print_interrupt_exit_log()
            pool.terminate()
        return


def main():
    aa = AlfarmAutomation('C:\\Users\\enmso\\Desktop\\올웨이즈.lnk')
    aa.automation_logic()
    return


if __name__ == '__main__':
    main()
    