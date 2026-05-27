@echo off
:: Проверка наличия EXE
if not exist "dist\MinecraftAutoClicker.exe" (
    echo ❌ Файл MinecraftAutoClicker.exe не найден!
    echo Убедитесь, что вы распаковали архив полностью.
    pause
    exit /b 1
)

:: Проверка запуска от администратора (опционально)
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️ Рекомендуется запускать от имени администратора для стабильной работы.
    timeout /t 2 >nul
)

:: Запуск программы
echo 🚀 Запуск Minecraft AutoClicker...
start "" "dist\MinecraftAutoClicker.exe"

:: Опционально: скрыть окно через 1 секунду
timeout /t 1 >nul
exit
