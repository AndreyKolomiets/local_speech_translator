mkdir -p $1 && { 
    python run_audio_saving.py --folder $1 & python run_translation.py --folder $1 --initial-prompt "$2" & python ui.py --folder $1
    }