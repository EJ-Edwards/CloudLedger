# Reflections

1. Share one aspect of building this project you found challenging and how you
   overcame it.

One challenge that I struggled with is how to get the credits website to my portfolio to work properly. I searched online and looked at examples and I was told to use the Rich library since its good for designing text and including hyperlinks into all modern terminals. I also looked at examples of how it worked and implemented into my own situation. It really pushed me to lock in even though I was giving up and in the end it was worth it because I learned something new that I never thought was even possible.


2. Share one technical concept that you gained a deeper understanding of
   through building this project. Explain that concept in simple terms and
   explain how it is used in your project.

One technical concept that I learned is that when you connect to a server via SSH, the server presents a host key to prove its identity, and the program has to verify that key to make sure it is accurate. If a program accepts any key without fact checking, an attacker can sit in the middle and perform a man-in-the-middle attack. When I was developing CloudLedger, I first used AutoAddPolicy, but then I realized it accepts any server without verification, which can only lead to man-in-the-middle attacks. I replaced it with my own policy that shows the user the server's fingerprint and asks them to confirm before connecting. When the user says yes, the host key gets saved to a file so it can be recognized the next time.