# fleet-ota

Updating ESP32 boards over Wi-Fi instead of plugging them in every time.

I have a few ESP32-C6 boards around my apartment and wanted a way to push new
firmware to all of them from my computer. This is a small server that holds the
firmware and tells the boards when there's a new version, plus the firmware on
the boards that downloads it and installs it. If an update is bad the board
should go back to the old version on its own.

Work in progress.

## Plan

- server that says what the latest version is and serves the file
- board connects to wifi and checks for updates
- actually do an update over the air
- rollback if the new firmware doesn't work
- keep track of each board and what version it's on
- sign the firmware so boards only accept mine
- test what happens if power gets cut mid-update

## Folders

- `server/` - python server (FastAPI)
- `firmware/` - code for the boards (C, ESP-IDF v6.1)

## Boards

Waveshare ESP32-C6-DEV-KIT-N8