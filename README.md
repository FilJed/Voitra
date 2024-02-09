Telegram bot, that helps transcribe and then sum up content of your voices and meetings.

# To dos
- limitation:
    - audiofiles more than 25mb
        - chunking
        - silence 
        - archiving
    - there is limit (technocal (4096 utf) and cognitive) on size of message sent back -- need to cut it wisely
- beautifying answers
- DevOps:
    - docker
        - refact it to 2 sage build with only venv
        - docker compose
    - CI/CD -- github action on push/merge
    - administration
        - logging
- performanse
    - ffmpeg - takes time for conversion
        - use python instead of cli
    - stream io -- less iops
- social functioanality
    - user accounting
    - statistic
- count channels to expect number of speaking persons


