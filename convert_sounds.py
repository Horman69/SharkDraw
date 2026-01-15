# -*- coding: utf-8 -*-
"""
Конвертер MP3 в WAV для звуков SharkDraw
Использует pydub для конвертации
"""

import os
from pathlib import Path

def convert_mp3_to_wav():
    """Конвертировать все MP3 файлы в WAV"""
    sounds_dir = Path('assets/sounds')
    
    if not sounds_dir.exists():
        print(f'❌ Папка {sounds_dir} не найдена')
        return
    
    # Проверяем наличие pydub
    try:
        from pydub import AudioSegment
    except ImportError:
        print('❌ Модуль pydub не установлен')
        print('\nУстановите командой:')
        print('  python -m pip install pydub')
        print('\n⚠️ Также требуется ffmpeg!')
        print('Скачайте: https://www.gyan.dev/ffmpeg/builds/')
        print('\nАльтернатива: используйте онлайн конвертер:')
        print('  https://cloudconvert.com/mp3-to-wav')
        return
    
    # Ищем MP3 файлы
    mp3_files = list(sounds_dir.glob('*.mp3'))
    
    if not mp3_files:
        print('✓ MP3 файлы не найдены, конвертация не требуется')
        return
    
    print(f'Найдено {len(mp3_files)} MP3 файлов для конвертации:\n')
    
    for mp3_file in mp3_files:
        wav_file = mp3_file.with_suffix('.wav')
        
        try:
            print(f'Конвертирую: {mp3_file.name} → {wav_file.name}...')
            audio = AudioSegment.from_mp3(str(mp3_file))
            audio.export(str(wav_file), format='wav')
            print(f'✓ Готово: {wav_file.name}')
            
        except Exception as e:
            print(f'❌ Ошибка при конвертации {mp3_file.name}: {e}')
    
    print('\n✅ Конвертация завершена!')
    print('Теперь можно запустить приложение.')

if __name__ == '__main__':
    print('=' * 50)
    print('🔊 Конвертер MP3 → WAV для SharkDraw')
    print('=' * 50)
    print()
    convert_mp3_to_wav()
