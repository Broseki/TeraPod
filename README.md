#<img src="https://raw.githubusercontent.com/mcanningjr/TeraPod/main/static/dist/img/TeraPod_logo.png" alt="TeraPod" width="250"/>
TeraPod is an opensource system for managing small, indoor greenhouses (i.e. "TeraPods"). This system is intended to
control heat, humidity, and lighting; and will be able to follow schedules which can be shared with other users. This is currently early in the development stage, and not ready at all for real use.

##TeraPod-OS
Currently unreleased is the TeraPod-OS Linux distro.
This is a Yocto based linux distro that runs on a Raspberry Pi. It connects to the TeraPod's sensors and relays
information back to the master server. This will be released in the near future.

##Disclaimer
This project makes no claim as to its the safety, stability, or efficacy. This is highly experimental and should
not be used to control things that are critical, or could cause fires or other damage. Because some of this code
is designed to run heaters, lights, and other potentially dangerous electrical devices you are running this at your
own risk, there is no promise that your property will not burn down or otherwise become damaged because of errors in
the design of TeraPod. **USE AT YOUR OWN RISK!**