# WSD-Extracts

This repository contains most of the code I wrote for this project.
Code written by other group members is not included.

The project is a website that can be found here:
https://quiet-everglades-45571.herokuapp.com

__HTML/CSS:__<br>
I wrote the base.html and base.css files that are extended by the other
html templates. These two files make the visual appearance of the website.
The other html documents are only used to render content for the base
files. All the other html files are also written by me.

__Graphics:__<br>
All the graphics that can be found on the website are my design.

__Tools:__<br>
A python method for calculating a checksum used in communicating
with the 'online payment service' used by the website. No money is
actually transferred by the said service. This was a school project,
after all.

__Backend:__<br>
_models.py:_ One of the models used by the website is entirely written
by me. This is the one used in tracking purchases and whether a user
can play a given game

_views.py:_ All the views responsible of handling transactions were written
by me. On top of that I created the statistics visible on some pages. As
those methods contain code written by my group members however,
I won't shown them here.

##### In a nutshell:
I wrote most of the stuff you see and, when you 'purchase' something,
what happens under the hood. These along with some minor things not worth
mentioning.