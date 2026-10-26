# OSMS

Учебный репозиторий по системам мобильной связи. Работы написаны на Python и относятся к темам лабораторных: дискретизация, квантование, спектральный анализ аудио и расчёт потерь в радиоканале.

## Что есть в проекте

- исследование дискретизации гармонического сигнала и влияния частоты дискретизации;
- сравнение спектров и оценка ошибки квантования для разной разрядности АЦП;
- анализ WAV-файла во временной и частотной областях;
- прореживание аудиосигнала и сравнение спектров до и после обработки;
- генерация простого музыкального фрагмента;
- добавление постоянного смещения к аудиосигналу;
- оценка MAPL, радиуса соты и количества базовых станций для заданной площади.

## Структура репозитория

```text
.
├── data/
│   └── audio/
│       ├── input.wav              # исходная аудиозапись
│       └── audacity_project.aup3  # проект Audacity
├── labs/
│   ├── lab01_sampling_quantization.py
│   ├── lab01_audio_analysis.py
│   ├── lab01_audio_generation.py
│   ├── lab01_audio_offset.py
│   └── lab02_radio_coverage       # расчёт радиопокрытия
├── outputs/
│   ├── audio/                     # сохранённые аудиофайлы
│   └── figures/                   # готовые графики
├── requirements.txt
└── README.md
```

## Скрипты

| Файл                                                                         | Назначение                                                         |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| [`labs/lab01_sampling_quantization.py`](labs/lab01_sampling_quantization.py) | Дискретизация гармонического сигнала, расчёт спектра и квантование |
| [`labs/lab01_audio_analysis.py`](labs/lab01_audio_analysis.py)               | Анализ WAV-файла, ручное ДПФ/БПФ и прореживание сигнала            |
| [`labs/lab01_audio_generation.py`](labs/lab01_audio_generation.py)           | Генерация и воспроизведение музыкального фрагмента                 |
| [`labs/lab01_audio_offset.py`](labs/lab01_audio_offset.py)                   | Добавление постоянного смещения и сохранение нового WAV-файла      |
| [`labs/lab02_radio_coverage`](labs/lab02_radio_coverage)                     | Расчёт потерь сигнала по моделям COST 231 и радиуса покрытия       |

## Установка

Нужен Python 3. Для установки библиотек выполните команды из корня репозитория:

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\activate        # Windows
python -m pip install -r requirements.txt
```

В проекте используются `numpy`, `scipy`, `matplotlib` и `sounddevice`. Для воспроизведения звука через `sounddevice` также может понадобиться установленная в системе библиотека PortAudio.

## Запуск

Все команды нужно выполнять из корня репозитория:

```bash
python labs/lab01_sampling_quantization.py
python labs/lab01_audio_analysis.py
python labs/lab01_audio_generation.py
python labs/lab01_audio_offset.py
python labs/lab02_radio_coverage
```

Графики открываются в окнах Matplotlib. Скрипт `lab01_audio_offset.py` дополнительно сохраняет обработанный файл в [`outputs/audio/offset.wav`](outputs/audio/offset.wav).

## Результаты

Готовые изображения находятся в каталоге [`outputs/figures/`](outputs/figures/):

- [`lab01_sampling.png`](outputs/figures/lab01_sampling.png) — сравнение исходного и дискретных сигналов;
- [`lab01_spectrum.png`](outputs/figures/lab01_spectrum.png) — спектральный анализ;
- [`lab01_quantization.png`](outputs/figures/lab01_quantization.png) — влияние разрядности квантования;
- [`lab01_waveform.png`](outputs/figures/lab01_waveform.png) — временная форма аудиосигнала;
- [`lab01_downsampling.png`](outputs/figures/lab01_downsampling.png) — результат прореживания;
- [`lab02_pathloss.png`](outputs/figures/lab02_pathloss.png) — потери сигнала в зависимости от расстояния.

Основные исходные данные для аудио находятся в `data/audio/input.wav`.
