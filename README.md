# stillCenter
Curated app store for stillOS

- stillCenter is stillOS software center with curated apps in order to only show apps that well on stillOS.
- Each app has a rating which allows shows how well it integrates into the system based on a criteria set.
- It uses a database called saDB which creates a SQlite database locally with the apps that the center can search very fast compared to AppStream (the standard app database for Linux). 
- To make package installation more stable, allow us to fix flatpak permission issues, and to eventually support DistroBox apps and web apps, we use a custom-made alternative to PackageKit called SAM. 
- SAM and SaDB combined make stillCenter a lot more reliable than other distro software centers.

![image](https://github.com/user-attachments/assets/394f756f-5e6a-4c96-9d23-c280327b3ebd)
![image](https://github.com/user-attachments/assets/2f39b203-fbc8-40cc-835e-862c21952cef)
![image](https://github.com/user-attachments/assets/b32211fa-c91d-4e99-8a3e-8cda362d62c0)

Dependencies:
- https://github.com/stillhq/SADB (database for apps in the store)
- https://github.com/stillhq/sam (packagekit alternative for app installation)
